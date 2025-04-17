from sqlalchemy import Column, String, Text, Float, Boolean, Time

from app.db.base import BaseModel


class CoffeeShopLocation(BaseModel):
    __tablename__ = "coffee_shop_locations"

    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    postal_code = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    opening_time = Column(Time, nullable=True)
    closing_time = Column(Time, nullable=True)

    def __repr__(self):
        return f"<CoffeeShopLocation {self.name}>"


class StaticInfo(BaseModel):
    __tablename__ = "static_info"

    key = Column(String, unique=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<StaticInfo {self.key}>"
