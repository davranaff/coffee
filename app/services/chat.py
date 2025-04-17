from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import chat_session, chat_message
from app.schemas import ChatSession, ChatSessionCreate, ChatMessage, ChatMessageCreate, ChatMessageUpdate

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_session(self, user_id: int) -> ChatSession:
        """Gets the active chat session of the user or creates a new one"""
        db_session = await chat_session.get_by_user(self.db, user_id=user_id)
        if not db_session:
            # Creates a new chat session
            session_data = ChatSessionCreate(user_id=user_id)
            db_session = await chat_session.create(self.db, obj_in=session_data)

        # Gets messages for the session
        messages = await chat_message.get_by_session(self.db, session_id=db_session.id)
        messages_data = [ChatMessage.from_orm(m) for m in messages]

        return ChatSession(
            id=db_session.id,
            user_id=db_session.user_id,
            is_active=db_session.is_active,
            created_at=db_session.created_at,
            updated_at=db_session.updated_at,
            messages=messages_data
        )

    async def add_message(self, user_id: int, message_text: str) -> ChatMessage:
        """Adds a new message from the user to the chat"""
        # Gets or creates a chat session
        session = await self.get_or_create_session(user_id)

        # Creates a new message
        message_data = ChatMessageCreate(content=message_text)
        db_message = await chat_message.create(
            self.db,
            obj_in={
                "content": message_data.content,
                "sender_id": user_id,
                "session_id": session.id,
                "is_read": False
            }
        )

        return ChatMessage.from_orm(db_message)

    async def add_staff_message(self, session_id: int, staff_id: int, message_text: str) -> ChatMessage:
        """Adds a message from a staff member to the chat"""
        # Checks the existence of the session
        db_session = await chat_session.get(self.db, id=session_id)
        if not db_session:
            raise ValueError("Chat session not found")

        # Creates a new message
        message_data = ChatMessageCreate(content=message_text)
        db_message = await chat_message.create(
            self.db,
            obj_in={
                "content": message_data.content,
                "sender_id": staff_id,
                "session_id": session_id,
                "is_read": False
            }
        )

        return ChatMessage.from_orm(db_message)

    async def get_messages(self, session_id: int, skip: int = 0, limit: int = 100) -> List[ChatMessage]:
        """Gets the list of messages for the chat session"""
        db_messages = await chat_message.get_by_session(
            self.db,
            session_id=session_id,
            skip=skip,
            limit=limit
        )

        return [ChatMessage.from_orm(m) for m in db_messages]

    async def mark_messages_as_read(self, session_id: int, user_id: int) -> bool:
        """Marks messages as read"""
        await chat_message.mark_as_read(self.db, session_id=session_id, sender_id=user_id)
        return True

    async def get_unread_count(self, session_id: int, user_id: int) -> int:
        """Gets the count of unread messages for the user"""
        # Gets unread messages not from the current user
        messages = await chat_message.get_unread(self.db, session_id=session_id)
        return len([m for m in messages if m.sender_id != user_id])

    async def close_session(self, session_id: int) -> bool:
        """Closes the chat session"""
        db_session = await chat_session.get(self.db, id=session_id)
        if not db_session:
            raise ValueError("Chat session not found")

        db_session.is_active = False
        self.db.add(db_session)
        await self.db.commit()
        return True

    async def get_active_sessions(self, skip: int = 0, limit: int = 100) -> List[ChatSession]:
        """Gets the list of active chat sessions (for administrators)"""
        db_sessions = await chat_session.get_active(self.db)

        result = []
        for session in db_sessions:
            # Gets messages for the session
            messages = await chat_message.get_by_session(
                self.db, 
                session_id=session.id,
                skip=0,
                limit=10  # Gets only the last 10 messages
            )
            messages_data = [ChatMessage.from_orm(m) for m in messages]

            session_data = ChatSession.from_orm(session)
            session_data.messages = messages_data
            result.append(session_data)

        return result
