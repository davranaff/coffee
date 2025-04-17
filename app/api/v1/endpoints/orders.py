from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models.user import User
from app.db.models.order import OrderStatus
from app.api.dependencies import get_current_active_user, get_current_active_staff
from app.services.order import OrderService
from app.schemas import Order

router = APIRouter()

@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    delivery_address: str = Body(...),
    contact_phone: str = Body(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new order from the user's cart.
    """
    try:
        order_service = OrderService(db)
        return await order_service.create_order(
            current_user.id,
            delivery_address=delivery_address,
            contact_phone=contact_phone
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[Order])
async def read_user_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the list of orders for the current user.
    """
    order_service = OrderService(db)
    return await order_service.get_orders(current_user.id, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=Order)
async def read_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get information about an order by ID.
    """
    try:
        order_service = OrderService(db)
        return await order_service.get_order(current_user.id, order_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.put("/{order_id}/cancel", response_model=Order)
async def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cancel an order by the user.
    """
    try:
        order_service = OrderService(db)
        return await order_service.cancel_order(current_user.id, order_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{order_id}/status", response_model=Order)
async def update_order_status(
    order_id: int,
    status: OrderStatus,
    current_user: User = Depends(get_current_active_staff),
    db: AsyncSession = Depends(get_db)
):
    """
    Update the status of an order (only for staff).
    """
    try:
        order_service = OrderService(db)
        return await order_service.update_order_status(order_id, status)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/admin/all", response_model=List[Order])
async def read_all_orders(
    skip: int = 0,
    limit: int = 100,
    status: OrderStatus = None,
    current_user: User = Depends(get_current_active_staff),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the list of all orders (only for staff).
    """
    from app.crud import order

    if status:
        db_orders = await order.get_by_status(db, status=status, skip=skip, limit=limit)
    else:
        query = None  # Use the default query
        db_orders = await order.get_multi(db, skip=skip, limit=limit, query=query)

    order_service = OrderService(db)
    result = []

    for db_order in db_orders:
        try:
            order_data = await order_service.get_order(db_order.user_id, db_order.id)
            result.append(order_data)
        except ValueError:
            continue

    return result
