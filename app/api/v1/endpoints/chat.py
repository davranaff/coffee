from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models.user import User
from app.api.dependencies import get_current_active_user, get_current_active_staff
from app.services.chat import ChatService
from app.schemas import ChatSession, ChatMessage, ChatMessageCreate

router = APIRouter()


@router.get("/session", response_model=ChatSession)
async def get_chat_session(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get or create a chat session for the current user.
    """
    chat_service = ChatService(db)
    return await chat_service.get_or_create_session(current_user.id)

@router.post("/messages", response_model=ChatMessage)
async def add_message(
    message: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a new message to the chat from the user.
    """
    chat_service = ChatService(db)
    return await chat_service.add_message(current_user.id, message.content)

@router.get("/messages/{session_id}", response_model=List[ChatMessage])
async def get_messages(
    session_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the messages of the chat session.
    """
    from app.crud import chat_session

    session = await chat_session.get(db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )

    if session.user_id != current_user.id and current_user.role not in ["admin", "staff"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No access to this chat session"
        )

    chat_service = ChatService(db)
    return await chat_service.get_messages(session_id, skip=skip, limit=limit)

@router.post("/messages/{session_id}/read", response_model=dict)
async def mark_messages_as_read(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark messages as read.
    """
    chat_service = ChatService(db)
    await chat_service.mark_messages_as_read(session_id, current_user.id)
    return {"message": "Messages marked as read"}

@router.get("/sessions/active", response_model=List[ChatSession])
async def get_active_sessions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_staff),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the list of active chat sessions (only for staff).
    """
    chat_service = ChatService(db)
    return await chat_service.get_active_sessions(skip=skip, limit=limit)

@router.post("/staff/messages/{session_id}", response_model=ChatMessage)
async def add_staff_message(
    session_id: int,
    message: ChatMessageCreate,
    current_user: User = Depends(get_current_active_staff),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a message from a staff member (only for staff).
    """
    try:
        chat_service = ChatService(db)
        return await chat_service.add_staff_message(
            session_id=session_id,
            staff_id=current_user.id,
            message_text=message.content
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/sessions/{session_id}/close", response_model=dict)
async def close_session(
    session_id: int,
    current_user: User = Depends(get_current_active_staff),
    db: AsyncSession = Depends(get_db)
):
    """
    Close the chat session (only for staff).
    """
    try:
        chat_service = ChatService(db)
        success = await chat_service.close_session(session_id)
        if success:
            return {"message": "Chat session closed"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
