from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models.info import CoffeeShopLocation, StaticInfo
from app.schemas.info import (
    CoffeeShopLocationCreate,
    CoffeeShopLocationUpdate,
    StaticInfoCreate,
    StaticInfoUpdate
)


class CRUDCoffeeShopLocation(CRUDBase[CoffeeShopLocation, CoffeeShopLocationCreate, CoffeeShopLocationUpdate]):
    async def get_by_city(
        self, db: AsyncSession, *, city: str, is_active: bool = True
    ) -> List[CoffeeShopLocation]:
        query = select(self.model).where(
            and_(
                self.model.city == city,
                self.model.is_active == is_active
            )
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_active(self, db: AsyncSession) -> List[CoffeeShopLocation]:
        query = select(self.model).where(self.model.is_active == True)
        result = await db.execute(query)
        return result.scalars().all()


class CRUDStaticInfo(CRUDBase[StaticInfo, StaticInfoCreate, StaticInfoUpdate]):
    async def get_by_key(self, db: AsyncSession, *, key: str) -> Optional[StaticInfo]:
        query = select(self.model).where(self.model.key == key)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession) -> List[StaticInfo]:
        query = select(self.model)
        result = await db.execute(query)
        return result.scalars().all()


coffee_shop_location = CRUDCoffeeShopLocation(CoffeeShopLocation)
static_info = CRUDStaticInfo(StaticInfo)
