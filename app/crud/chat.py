from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models.chat import ChatSession, ChatMessage
from app.schemas.chat import ChatSessionCreate, ChatMessageCreate, ChatMessageUpdate


class CRUDChatSession(CRUDBase[ChatSession, ChatSessionCreate, ChatSessionCreate]):
    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, is_active: bool = True
    ) -> Optional[ChatSession]:
        query = select(self.model).where(
            and_(
                self.model.user_id == user_id,
                self.model.is_active == is_active
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_active(self, db: AsyncSession) -> List[ChatSession]:
        query = select(self.model).where(self.model.is_active == True)
        result = await db.execute(query)
        return result.scalars().all()


class CRUDChatMessage(CRUDBase[ChatMessage, ChatMessageCreate, ChatMessageUpdate]):
    async def get_by_session(
        self, db: AsyncSession, *, session_id: int, skip: int = 0, limit: int = 100
    ) -> List[ChatMessage]:
        query = (
            select(self.model)
            .where(self.model.session_id == session_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_unread(
        self, db: AsyncSession, *, session_id: int, skip: int = 0, limit: int = 100
    ) -> List[ChatMessage]:
        query = (
            select(self.model)
            .where(
                and_(
                    self.model.session_id == session_id,
                    self.model.is_read == False
                )
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def mark_as_read(
        self, db: AsyncSession, *, session_id: int, sender_id: int
    ) -> None:
        query = select(self.model).where(
            and_(
                self.model.session_id == session_id,
                self.model.sender_id != sender_id,
                self.model.is_read == False
            )
        )
        result = await db.execute(query)
        messages = result.scalars().all()
        for message in messages:
            message.is_read = True
            db.add(message)
        await db.commit()


chat_session = CRUDChatSession(ChatSession)
chat_message = CRUDChatMessage(ChatMessage)
