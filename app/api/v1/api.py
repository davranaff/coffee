from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth, users, products, cart, orders, chat, info
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(cart.router, prefix="/cart", tags=["cart"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(info.router, prefix="/info", tags=["info"])
