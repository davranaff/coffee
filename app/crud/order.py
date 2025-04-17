from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    async def get_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_status(
        self, db: AsyncSession, *, status: OrderStatus, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        query = (
            select(self.model)
            .where(self.model.status == status)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def create_with_items(
        self, db: AsyncSession, *, obj_in: OrderCreate
    ) -> Order:
        order = await self.create(db, obj_in=obj_in)

        for item in obj_in.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price
            )
            db.add(order_item)

        await db.commit()
        await db.refresh(order)
        return order


class CRUDOrderItem(CRUDBase[OrderItem, OrderItemCreate, OrderItemCreate]):
    async def get_by_order(
        self, db: AsyncSession, *, order_id: int, skip: int = 0, limit: int = 100
    ) -> List[OrderItem]:
        query = (
            select(self.model)
            .where(self.model.order_id == order_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()


order = CRUDOrder(Order)
order_item = CRUDOrderItem(OrderItem)
