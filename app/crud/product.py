from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models.product import Category, Product
from app.schemas.product import CategoryCreate, CategoryUpdate, ProductCreate, ProductUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Category]:
        query = select(self.model).where(self.model.name == name)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_active(self, db: AsyncSession) -> List[Category]:
        query = select(self.model).where(self.model.is_active == True)
        result = await db.execute(query)
        return result.scalars().all()


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Product]:
        query = select(self.model).where(self.model.name == name)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_category(
        self, db: AsyncSession, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        query = (
            select(self.model)
            .where(self.model.category_id == category_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def search(
        self,
        db: AsyncSession,
        *,
        query: Optional[str] = None,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        is_available: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Product]:
        conditions = []

        if query:
            conditions.append(self.model.name.ilike(f"%{query}%"))

        if category_id:
            conditions.append(self.model.category_id == category_id)

        if min_price is not None:
            conditions.append(self.model.price >= min_price)

        if max_price is not None:
            conditions.append(self.model.price <= max_price)

        if is_available is not None:
            conditions.append(self.model.is_available == is_available)

        query = select(self.model)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    async def get_available(self, db: AsyncSession) -> List[Product]:
        query = select(self.model).where(self.model.is_available == True)
        result = await db.execute(query)
        return result.scalars().all()


category = CRUDCategory(Category)
product = CRUDProduct(Product)
