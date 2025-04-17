from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models.user import User
from app.api.dependencies import get_current_active_user
from app.services.cart import CartService
from app.schemas import Cart, CartItem, CartItemCreate, CartItemUpdate

router = APIRouter()

@router.get("/", response_model=Cart)
async def read_cart(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user's cart.
    """
    cart_service = CartService(db)
    return await cart_service.get_user_cart(current_user.id)

@router.post("/items", response_model=CartItem, status_code=status.HTTP_201_CREATED)
async def add_cart_item(
    item_in: CartItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add an item to the cart.
    """
    try:
        cart_service = CartService(db)
        return await cart_service.add_item(current_user.id, item_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/items/{item_id}", response_model=CartItem)
async def update_cart_item(
    item_id: int,
    item_in: CartItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update the quantity of an item in the cart.
    """
    try:
        cart_service = CartService(db)
        return await cart_service.update_item(current_user.id, item_id, item_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/items/{item_id}", response_model=dict)
async def remove_cart_item(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove an item from the cart.
    """
    try:
        cart_service = CartService(db)
        success = await cart_service.remove_item(current_user.id, item_id)
        if success:
            return {"message": "Item successfully removed from cart"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/", response_model=dict)
async def clear_cart(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Clear the cart.
    """
    try:
        cart_service = CartService(db)
        success = await cart_service.clear_cart(current_user.id)
        if success:
            return {"message": "Cart successfully cleared"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
