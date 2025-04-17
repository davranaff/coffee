from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import cart, cart_item, product
from app.schemas import Cart, CartItem, CartItemCreate, CartItemUpdate, Product


class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_cart(self, user_id: int) -> Cart:
        """Gets or creates a cart for the user"""
        db_cart = await cart.get_or_create(self.db, user_id=user_id)

        cart_items = await cart_item.get_by_cart(self.db, cart_id=db_cart.id)
        cart_items_with_products = []

        for item in cart_items:
            db_product = await product.get(self.db, id=item.product_id)
            if db_product and db_product.is_available:
                product_data = Product.from_orm(db_product)
                cart_item_data = CartItem.from_orm(item)
                cart_items_with_products.append({
                    **cart_item_data.dict(),
                    "product": product_data
                })

        return Cart(
            id=db_cart.id,
            user_id=db_cart.user_id,
            created_at=db_cart.created_at,
            updated_at=db_cart.updated_at,
            items=cart_items_with_products
        )

    async def add_item(self, user_id: int, item_in: CartItemCreate) -> CartItem:
        """Adds a product to the cart"""
        # Check product existence
        db_product = await product.get(self.db, id=item_in.product_id)
        if not db_product:
            raise ValueError("Product not found")

        if not db_product.is_available:
            raise ValueError("Product unavailable")

        # Get or create cart
        db_cart = await cart.get_or_create(self.db, user_id=user_id)

        # Check if the product is already in the cart
        existing_item = await cart_item.get_by_cart_and_product(
            self.db,
            cart_id=db_cart.id,
            product_id=item_in.product_id
        )

        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + item_in.quantity
            updated_item = await cart_item.update_quantity(
                self.db, 
                cart_item=existing_item, 
                quantity=new_quantity
            )
            return CartItem.from_orm(updated_item)
        else:
            # Create a new product in the cart
            item_data = CartItemCreate(
                product_id=item_in.product_id,
                quantity=item_in.quantity
            )

            new_cart_item = await cart_item.create(
                self.db,
                obj_in=CartItemCreate(
                    cart_id=db_cart.id,
                    product_id=item_data.product_id,
                    quantity=item_data.quantity
                )
            )

            return CartItem.from_orm(new_cart_item)

    async def update_item(self, user_id: int, item_id: int, item_in: CartItemUpdate) -> CartItem:
        """Updates the quantity of a product in the cart"""
        # Get user cart
        db_cart = await cart.get_by_user(self.db, user_id=user_id)
        if not db_cart:
            raise ValueError("Cart not found")

        # Get cart item
        db_cart_item = await cart_item.get(self.db, id=item_id)
        if not db_cart_item or db_cart_item.cart_id != db_cart.id:
            raise ValueError("Cart item not found")

        # Update quantity
        updated_item = await cart_item.update_quantity(
            self.db,
            cart_item=db_cart_item,
            quantity=item_in.quantity
        )

        return CartItem.from_orm(updated_item)

    async def remove_item(self, user_id: int, item_id: int) -> bool:
        """Removes a product from the cart"""
        # Get user cart
        db_cart = await cart.get_by_user(self.db, user_id=user_id)
        if not db_cart:
            raise ValueError("Cart not found")

        # Get cart item
        db_cart_item = await cart_item.get(self.db, id=item_id)
        if not db_cart_item or db_cart_item.cart_id != db_cart.id:
            raise ValueError("Cart item not found")

        # Remove item
        await cart_item.remove(self.db, id=item_id)
        return True

    async def clear_cart(self, user_id: int) -> bool:
        """Clears the user's cart"""
        # Get user cart
        db_cart = await cart.get_by_user(self.db, user_id=user_id)
        if not db_cart:
            raise ValueError("Cart not found")

        # Remove all items from the cart
        await cart_item.remove_by_cart(self.db, cart_id=db_cart.id)
        return True
