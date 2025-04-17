from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    price: float

    @validator("quantity")
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v

    @validator("price")
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)


class OrderItem(OrderItemBase):
    id: int
    order_id: int
    price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderItemWithProduct(OrderItem):
    pass


class OrderBase(BaseModel):
    status: str = "pending"
    total_amount: float = Field(..., ge=0)
    shipping_address: str
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    shipping_address: Optional[str] = None
    notes: Optional[str] = None


class Order(OrderBase):
    id: int
    user_id: int
    items: List[OrderItem]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
