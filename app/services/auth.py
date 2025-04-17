from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, create_refresh_token, decode_token
from app.crud import user
from app.schemas import Token, User, UserCreate, UserVerify


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, user_in: UserCreate) -> User:
        db_user = await user.get_by_email(self.db, email=user_in.email)
        if db_user:
            raise ValueError("Email already registered")

        db_user = await user.create(self.db, obj_in=user_in)
        return User.from_orm(db_user)

    async def login(self, email: str, password: str) -> Token:
        db_user = await user.authenticate(self.db, email=email, password=password)
        if not db_user:
            raise ValueError("Incorrect email or password")
        if not user.is_active(db_user):
            raise ValueError("Inactive user")

        return Token(
            access_token=create_access_token(str(db_user.id)),
            refresh_token=create_refresh_token(str(db_user.id))
        )

    async def verify(self, verify_in: UserVerify) -> bool:
        db_user = await user.get_by_email(self.db, email=verify_in.email)
        if not db_user:
            raise ValueError("User not found")

        if db_user.verification_code != verify_in.verification_code:
            raise ValueError("Invalid verification code")

        if db_user.verification_code_expires < datetime.utcnow():
            raise ValueError("Verification code expired")

        db_user.is_verified = True
        db_user.verification_code = None
        db_user.verification_code_expires = None
        self.db.add(db_user)
        await self.db.commit()
        return True

    async def refresh_token(self, refresh_token: str) -> Token:
        try:
            payload = decode_token(refresh_token)
            if payload["type"] != "refresh":
                raise ValueError("Invalid token type")

            db_user = await user.get(self.db, id=int(payload["sub"]))
            if not db_user:
                raise ValueError("User not found")

            return Token(
                access_token=create_access_token(str(db_user.id)),
                refresh_token=create_refresh_token(str(db_user.id))
            )
        except Exception as e:
            raise ValueError("Invalid refresh token")
