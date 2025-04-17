from sqlalchemy import Boolean, Column, String, DateTime
from enum import Enum as PyEnum

from app.db.base import BaseModel


class UserRole(str, PyEnum):
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_code = Column(String, nullable=True)
    verification_code_expires = Column(DateTime, nullable=True)
    role = Column(String, default=UserRole.USER, nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"
