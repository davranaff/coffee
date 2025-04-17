from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class WebSocketMessage(BaseModel):
    """Schema for WebSocket messages"""
    session_id: int
    content: str
    sender: str
    timestamp: datetime = None


class ChatMessageBase(BaseModel):
    content: str
    sender_id: int
    session_id: int
    is_read: bool = False


class ChatMessageCreate(BaseModel):
    content: str


class ChatMessageUpdate(BaseModel):
    is_read: bool = True


class ChatMessageInDB(ChatMessageBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChatMessage(ChatMessageInDB):
    pass


class ChatSessionBase(BaseModel):
    user_id: int
    is_active: bool = True


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    is_active: Optional[bool] = None


class ChatSessionInDB(ChatSessionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatSession(ChatSessionInDB):
    messages: List[ChatMessage] = []
