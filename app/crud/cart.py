from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models.cart import Cart, CartItem
from app.schemas.cart import CartCreate, CartItemCreate, CartItemUpdate


class CRUDCart(CRUDBase[Cart, CartCreate, CartCreate]):
    async def get_by_user(self, db: AsyncSession, *, user_id: int) -> Optional[Cart]:
        query = select(self.model).where(self.model.user_id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_or_create(self, db: AsyncSession, *, user_id: int) -> Cart:
        cart = await self.get_by_user(db, user_id=user_id)
        if not cart:
            cart = await self.create(db, obj_in=CartCreate(user_id=user_id))
        return cart


class CRUDCartItem(CRUDBase[CartItem, CartItemCreate, CartItemUpdate]):
    async def get_by_cart_and_product(
        self, db: AsyncSession, *, cart_id: int, product_id: int
    ) -> Optional[CartItem]:
        query = select(self.model).where(
            and_(
                self.model.cart_id == cart_id,
                self.model.product_id == product_id
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_cart(
        self, db: AsyncSession, *, cart_id: int, skip: int = 0, limit: int = 100
    ) -> List[CartItem]:
        query = (
            select(self.model)
            .where(self.model.cart_id == cart_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def update_quantity(
        self, db: AsyncSession, *, cart_item: CartItem, quantity: int
    ) -> CartItem:
        cart_item.quantity = quantity
        db.add(cart_item)
        await db.commit()
        await db.refresh(cart_item)
        return cart_item

    async def remove_by_cart(self, db: AsyncSession, *, cart_id: int) -> None:
        query = select(self.model).where(self.model.cart_id == cart_id)
        result = await db.execute(query)
        items = result.scalars().all()
        for item in items:
            await db.delete(item)
        await db.commit()


cart = CRUDCart(Cart)
cart_item = CRUDCartItem(CartItem)
