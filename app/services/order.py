from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import order, order_item, product, cart, cart_item
from app.db.models.order import OrderStatus
from app.schemas import Order, OrderCreate, OrderUpdate, OrderItemCreate


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, user_id: int, delivery_address: str, contact_phone: str) -> Order:
        """Creates a new order from the user's cart"""
        # Get the user's cart
        db_cart = await cart.get_by_user(self.db, user_id=user_id)
        if not db_cart:
            raise ValueError("Cart not found")

        # Get the items in the cart
        cart_items = await cart_item.get_by_cart(self.db, cart_id=db_cart.id)
        if not cart_items:
            raise ValueError("Cart is empty")

        # Prepare order items and calculate the total amount
        total_amount = 0
        order_items_data = []

        for item in cart_items:
            # Get the product for availability and price check
            db_product = await product.get(self.db, id=item.product_id)
            if not db_product:
                raise ValueError(f"Product with ID {item.product_id} not found")

            if not db_product.is_available:
                raise ValueError(f"Product '{db_product.name}' is unavailable")

            # Create an order item
            item_price = db_product.price
            item_total = item_price * item.quantity
            total_amount += item_total

            order_items_data.append(OrderItemCreate(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item_price
            ))

        # Create the order with items
        order_data = OrderCreate(
            user_id=user_id,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
            delivery_address=delivery_address,
            contact_phone=contact_phone,
            items=order_items_data
        )

        # Create the order in the DB
        db_order = await order.create_with_items(self.db, obj_in=order_data)

        # Clear the cart
        await cart_item.remove_by_cart(self.db, cart_id=db_cart.id)

        # Get the full order data with items
        return await self.get_order(user_id, db_order.id)

    async def get_orders(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Gets the list of user's orders"""
        db_orders = await order.get_by_user(self.db, user_id=user_id, skip=skip, limit=limit)

        result = []
        for db_order in db_orders:
            # Get the order items
            db_order_items = await order_item.get_by_order(self.db, order_id=db_order.id)

            # Form order items with product data
            order_items_data = []
            for item in db_order_items:
                db_product = await product.get(self.db, id=item.product_id)
                if db_product:
                    product_data = {
                        "id": db_product.id,
                        "name": db_product.name,
                        "price": db_product.price,
                        "description": db_product.description,
                        "image_url": db_product.image_url,
                        "category_id": db_product.category_id,
                        "is_available": db_product.is_available,
                        "created_at": db_product.created_at,
                        "updated_at": db_product.updated_at
                    }

                    order_items_data.append({
                        "id": item.id,
                        "order_id": item.order_id,
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "price": item.price,
                        "created_at": item.created_at,
                        "updated_at": item.updated_at,
                        "product": product_data
                    })

            # Form the order with items
            order_data = {
                "id": db_order.id,
                "user_id": db_order.user_id,
                "status": db_order.status,
                "total_amount": db_order.total_amount,
                "delivery_address": db_order.delivery_address,
                "contact_phone": db_order.contact_phone,
                "created_at": db_order.created_at,
                "updated_at": db_order.updated_at,
                "items": order_items_data
            }

            result.append(order_data)

        return result

    async def get_order(self, user_id: int, order_id: int) -> Order:
        """Gets the order details"""
        db_order = await order.get(self.db, id=order_id)
        if not db_order:
            raise ValueError("Order not found")

        # Check if the order belongs to the user
        if db_order.user_id != user_id:
            raise ValueError("No access to the order")

        # Get the order items
        db_order_items = await order_item.get_by_order(self.db, order_id=db_order.id)

        # Form order items with product data
        order_items_data = []
        for item in db_order_items:
            db_product = await product.get(self.db, id=item.product_id)
            if db_product:
                product_data = {
                    "id": db_product.id,
                    "name": db_product.name,
                    "price": db_product.price,
                    "description": db_product.description,
                    "image_url": db_product.image_url,
                    "category_id": db_product.category_id,
                    "is_available": db_product.is_available,
                    "created_at": db_product.created_at,
                    "updated_at": db_product.updated_at
                }

                order_items_data.append({
                    "id": item.id,
                    "order_id": item.order_id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price,
                    "created_at": item.created_at,
                    "updated_at": item.updated_at,
                    "product": product_data
                })

        # Form the order with items
        return Order(
            id=db_order.id,
            user_id=db_order.user_id,
            status=db_order.status,
            total_amount=db_order.total_amount,
            delivery_address=db_order.delivery_address,
            contact_phone=db_order.contact_phone,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at,
            items=order_items_data
        )

    async def update_order_status(self, order_id: int, status: OrderStatus) -> Order:
        """Updates the order status (for administrators)"""
        db_order = await order.get(self.db, id=order_id)
        if not db_order:
            raise ValueError("Order not found")

        # Update the status
        update_data = OrderUpdate(status=status)
        updated_order = await order.update(self.db, db_obj=db_order, obj_in=update_data)

        # Get the updated order with items
        return await self.get_order(updated_order.user_id, updated_order.id)

    async def cancel_order(self, user_id: int, order_id: int) -> Order:
        """Cancels the user's order"""
        db_order = await order.get(self.db, id=order_id)
        if not db_order:
            raise ValueError("Order not found")

        # Check if the order belongs to the user
        if db_order.user_id != user_id:
            raise ValueError("No access to the order")

        # Check if the order can be cancelled
        if db_order.status not in [OrderStatus.PENDING, OrderStatus.PROCESSING]:
            raise ValueError("Order cannot be cancelled in its current status")

        # Update the status to "cancelled"
        update_data = OrderUpdate(status=OrderStatus.CANCELLED)
        updated_order = await order.update(self.db, db_obj=db_order, obj_in=update_data)

        # Get the updated order with items
        return await self.get_order(user_id, updated_order.id)
