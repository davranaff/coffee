from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime

from app.schemas.product import Product


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class CartItemCreate(CartItemBase):
    @validator("quantity")
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)

    @validator("quantity")
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v


class CartItem(CartItemBase):
    id: int
    cart_id: int
    price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CartItemWithProduct(CartItem):
    product: Product


class CartBase(BaseModel):
    total_amount: float = Field(0, ge=0)


class CartCreate(CartBase):
    pass


class CartInDB(CartBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Cart(CartInDB):
    items: List[CartItemWithProduct] = []
