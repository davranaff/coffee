from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.base import get_db
from app.api.dependencies import get_current_active_staff
from app.services.product import ProductService
from app.schemas import (
    Category, CategoryCreate,
    Product, ProductCreate, ProductUpdate
)

router = APIRouter()

# Categories
@router.get("/categories", response_model=List[Category])
async def read_categories(
    db: AsyncSession = Depends(get_db)
):
    """
    Get the list of all categories.
    """
    product_service = ProductService(db)
    return await product_service.get_categories()

@router.get("/categories/{category_id}", response_model=Category)
async def read_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get information about a category by ID.
    """
    try:
        product_service = ProductService(db)
        return await product_service.get_category(category_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_staff)
):
    """
    Create a new category (only for staff).
    """
    product_service = ProductService(db)
    return await product_service.create_category(category_in)

# Products
@router.get("/", response_model=List[Product])
async def read_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the list of all products with filtering and search capabilities.
    """
    product_service = ProductService(db)
    return await product_service.get_products(
        skip=skip,
        limit=limit,
        category_id=category_id,
        search=search
    )

@router.get("/{product_id}", response_model=Product)
async def read_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get information about a product by ID.
    """
    try:
        product_service = ProductService(db)
        return await product_service.get_product(product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_staff)
):
    """
    Create a new product (only for staff).
    """
    try:
        product_service = ProductService(db)
        return await product_service.create_product(product_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_staff)
):
    """
    Update a product (only for staff).
    """
    try:
        product_service = ProductService(db)
        return await product_service.update_product(product_id, product_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{product_id}", response_model=dict)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_staff)
):
    """
    Delete a product (only for staff).
    """
    try:
        product_service = ProductService(db)
        success = await product_service.delete_product(product_id)
        if success:
            return {"message": "Product successfully deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
