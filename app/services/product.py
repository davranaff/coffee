from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import category, product
from app.schemas import Category, CategoryCreate, Product, ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Category methods
    async def create_category(self, category_in: CategoryCreate) -> Category:
        db_category = await category.create(self.db, obj_in=category_in)
        return Category.from_orm(db_category)

    async def get_categories(self) -> List[Category]:
        db_categories = await category.get_active(self.db)
        return [Category.from_orm(c) for c in db_categories]

    async def get_category(self, category_id: int) -> Category:
        db_category = await category.get(self.db, id=category_id)
        if not db_category:
            raise ValueError("Category not found")
        return Category.from_orm(db_category)

    # Product methods
    async def create_product(self, product_in: ProductCreate) -> Product:
        db_category = await category.get(self.db, id=product_in.category_id)
        if not db_category:
            raise ValueError("Category not found")

        db_product = await product.create(self.db, obj_in=product_in)
        return Product.from_orm(db_product)

    async def get_products(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[Product]:
        db_products = await product.search(
            self.db,
            skip=skip,
            limit=limit,
            category_id=category_id,
            search=search
        )
        return [Product.from_orm(p) for p in db_products]

    async def get_product(self, product_id: int) -> Product:
        db_product = await product.get(self.db, id=product_id)
        if not db_product:
            raise ValueError("Product not found")
        return Product.from_orm(db_product)

    async def update_product(self, product_id: int, product_in: ProductUpdate) -> Product:
        db_product = await product.get(self.db, id=product_id)
        if not db_product:
            raise ValueError("Product not found")

        if product_in.category_id:
            db_category = await category.get(self.db, id=product_in.category_id)
            if not db_category:
                raise ValueError("Category not found")

        db_product = await product.update(self.db, db_obj=db_product, obj_in=product_in)
        return Product.from_orm(db_product)

    async def delete_product(self, product_id: int) -> bool:
        db_product = await product.get(self.db, id=product_id)
        if not db_product:
            raise ValueError("Product not found")

        await product.remove(self.db, id=product_id)
        return True
