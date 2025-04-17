from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import coffee_shop_location, static_info
from app.schemas import (
    CoffeeShopLocation, CoffeeShopLocationCreate, CoffeeShopLocationUpdate,
    StaticInfo, StaticInfoCreate, StaticInfoUpdate, CompanyInfo
)


class InfoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Methods for working with coffee shop locations
    async def create_location(self, location_in: CoffeeShopLocationCreate) -> CoffeeShopLocation:
        """Creates a new coffee shop location"""
        db_location = await coffee_shop_location.create(self.db, obj_in=location_in)
        return CoffeeShopLocation.from_orm(db_location)

    async def get_locations(self, city: Optional[str] = None) -> List[CoffeeShopLocation]:
        """Gets the list of coffee shop locations, optionally filtering by city"""
        if city:
            db_locations = await coffee_shop_location.get_by_city(self.db, city=city)
        else:
            db_locations = await coffee_shop_location.get_active(self.db)

        return [CoffeeShopLocation.from_orm(loc) for loc in db_locations]

    async def get_location(self, location_id: int) -> CoffeeShopLocation:
        """Gets information about a specific coffee shop location"""
        db_location = await coffee_shop_location.get(self.db, id=location_id)
        if not db_location:
            raise ValueError("Location not found")

        return CoffeeShopLocation.from_orm(db_location)

    async def update_location(
        self, location_id: int, location_in: CoffeeShopLocationUpdate
    ) -> CoffeeShopLocation:
        """Updates information about a coffee shop location"""
        db_location = await coffee_shop_location.get(self.db, id=location_id)
        if not db_location:
            raise ValueError("Location not found")

        db_location = await coffee_shop_location.update(
            self.db, db_obj=db_location, obj_in=location_in
        )

        return CoffeeShopLocation.from_orm(db_location)

    # Methods for working with static information
    async def create_static_info(self, info_in: StaticInfoCreate) -> StaticInfo:
        """Creates a new static information record"""
        # Checks if a record with such a key exists
        existing = await static_info.get_by_key(self.db, key=info_in.key)
        if existing:
            raise ValueError(f"Record with key '{info_in.key}' already exists")

        db_info = await static_info.create(self.db, obj_in=info_in)
        return StaticInfo.from_orm(db_info)

    async def get_static_info(self, key: str) -> StaticInfo:
        """Gets a static information record by key"""
        db_info = await static_info.get_by_key(self.db, key=key)
        if not db_info:
            raise ValueError(f"Information with key '{key}' not found")

        return StaticInfo.from_orm(db_info)

    async def update_static_info(
        self, key: str, info_in: StaticInfoUpdate
    ) -> StaticInfo:
        """Updates a static information record"""
        db_info = await static_info.get_by_key(self.db, key=key)
        if not db_info:
            raise ValueError(f"Information with key '{key}' not found")

        db_info = await static_info.update(self.db, db_obj=db_info, obj_in=info_in)
        return StaticInfo.from_orm(db_info)

    async def get_all_static_info(self) -> Dict[str, str]:
        """Gets all static information in the form of a key-value dictionary"""
        db_info_list = await static_info.get_all(self.db)
        return {info.key: info.value for info in db_info_list}

    async def get_company_info(self) -> CompanyInfo:
        """Gets general information about the company"""
        info_dict = await self.get_all_static_info()
        locations = await self.get_locations()

        # Gets company data from static information or uses default values
        name = info_dict.get("company_name", "Coffee Shop")
        description = info_dict.get("company_description", "")
        phone = info_dict.get("company_phone", "")
        email = info_dict.get("company_email", "")
        website = info_dict.get("company_website", "")

        # Gets social media data
        social_media = {
            "facebook": info_dict.get("social_facebook", ""),
            "instagram": info_dict.get("social_instagram", ""),
            "twitter": info_dict.get("social_twitter", "")
        }

        return CompanyInfo(
            name=name,
            description=description,
            phone=phone,
            email=email,
            website=website,
            social_media=social_media,
            locations=locations
        )
