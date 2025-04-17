from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.services.auth import AuthService
from app.schemas import Token, UserCreate, UserVerify

router = APIRouter()


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Registers a new user.
    """
    try:
        auth_service = AuthService(db)
        user = await auth_service.register(user_in)
        return {"message": "User successfully registered", "email": user.email}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    User authentication and token retrieval.
    """
    try:
        auth_service = AuthService(db)
        return await auth_service.login(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/verify", response_model=dict)
async def verify_email(
    verify_data: UserVerify,
    db: AsyncSession = Depends(get_db)
):
    """
    Email verification by code.
    """
    try:
        auth_service = AuthService(db)
        success = await auth_service.verify(verify_data)
        if success:
            return {"message": "Email successfully verified"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Access token refresh using the refresh token.
    """
    try:
        auth_service = AuthService(db)
        return await auth_service.refresh_token(refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
