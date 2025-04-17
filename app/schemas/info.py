from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, time


class CoffeeShopLocationBase(BaseModel):
    name: str
    address: str
    city: str
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: bool = True
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None


class CoffeeShopLocationCreate(CoffeeShopLocationBase):
    pass


class CoffeeShopLocationUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None


class CoffeeShopLocationInDB(CoffeeShopLocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CoffeeShopLocation(CoffeeShopLocationInDB):
    pass


class StaticInfoBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None


class StaticInfoCreate(StaticInfoBase):
    pass


class StaticInfoUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None


class StaticInfoInDB(StaticInfoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StaticInfo(StaticInfoInDB):
    pass


class CompanyInfo(BaseModel):
    name: str
    description: str
    phone: str
    email: str
    website: str
    social_media: dict
    locations: List[CoffeeShopLocation]
