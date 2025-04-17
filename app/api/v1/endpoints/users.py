from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models.user import User
from app.api.dependencies import get_current_active_user, get_current_active_admin
from app.schemas import User as UserSchema, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get information about the current user.
    """
    return current_user

@router.put("/me", response_model=UserSchema)
async def update_user_me(user_in: UserUpdate, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    """
    Update the current user's data.
    """
    from app.crud.user import user
    try:
        updated_user = await user.update(db, db_obj=current_user, obj_in=user_in)
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{user_id}", response_model=UserSchema)
async def read_user_by_id(user_id: int, current_user: User = Depends(get_current_active_admin), db: AsyncSession = Depends(get_db)):
    """
    Get a user by ID (only for administrators).
    """
    from app.crud.user import user
    user_obj = await user.get(db, id=user_id)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_obj

@router.get("/", response_model=list[UserSchema])
async def read_users(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_active_admin), db: AsyncSession = Depends(get_db)):
    """
    Get the list of all users (only for administrators).
    """
    from app.crud.user import user
    from sqlalchemy import select
    users = await user.get_multi(db, skip=skip, limit=limit, query=select(User))
    return users
