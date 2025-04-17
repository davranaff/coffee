from typing import Dict
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.services.chat import ChatService
from app.schemas import WebSocketMessage


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: int, user_id: int):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = {}
        self.active_connections[session_id][user_id] = websocket

    def disconnect(self, session_id: int, user_id: int):
        if session_id in self.active_connections and user_id in self.active_connections[session_id]:
            del self.active_connections[session_id][user_id]
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def send_personal_message(self, message: str, session_id: int, user_id: int):
        if session_id in self.active_connections and user_id in self.active_connections[session_id]:
            websocket = self.active_connections[session_id][user_id]
            await websocket.send_text(message)

    async def broadcast(self, message: str, session_id: int):
        if session_id in self.active_connections:
            for user_id, websocket in self.active_connections[session_id].items():
                await websocket.send_text(message)


manager = ConnectionManager()


async def get_token_data(token: str):
    from app.core.security import decode_token
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return payload
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def get_user_by_token(token: str, db: AsyncSession):
    from app.db.models.user import User
    payload = await get_token_data(token)
    user_id = int(payload.get("sub"))
    user = await db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


async def websocket_endpoint(
    websocket: WebSocket,
    session_id: int,
    token: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        user = await get_user_by_token(token, db)
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    from app.crud import chat_session
    session = await chat_session.get(db, id=session_id)
    if not session:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    is_staff = user.role in ["admin", "staff"]
    if session.user_id != user.id and not is_staff:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, session_id, user.id)

    try:
        chat_service = ChatService(db)
        status_message = WebSocketMessage(
            message=f"User {user.email} connected to the chat",
            session_id=session_id,
            timestamp=datetime.utcnow()
        )
        await manager.broadcast(status_message.json(), session_id)
        while True:
            message_text = await websocket.receive_text()
            if is_staff:
                chat_message = await chat_service.add_staff_message(
                    session_id=session_id,
                    staff_id=user.id,
                    message_text=message_text
                )
            else:
                chat_message = await chat_service.add_message(
                    user_id=user.id,
                    message_text=message_text
                )
            out_message = WebSocketMessage(
                message=message_text,
                session_id=session_id,
                timestamp=chat_message.created_at
            )
            await manager.broadcast(out_message.json(), session_id)
    except WebSocketDisconnect:
        manager.disconnect(session_id, user.id)
        status_message = WebSocketMessage(
            message=f"User {user.email} disconnected from the chat",
            session_id=session_id,
            timestamp=datetime.utcnow()
        )
        await manager.broadcast(status_message.json(), session_id)
