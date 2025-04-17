from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models.user import User
from app.api.dependencies import get_current_active_staff
from app.services.info import InfoService
from app.schemas import (
    CoffeeShopLocation, CoffeeShopLocationCreate, CoffeeShopLocationUpdate,
    StaticInfo, StaticInfoCreate, StaticInfoUpdate, CompanyInfo
)

router = APIRouter()

# Coffee Shop Locations
@router.get("/locations", response_model=List[CoffeeShopLocation])
async def read_locations(
    city: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the list of coffee shop locations, optionally filtering by city.
    """
    info_service = InfoService(db)
    return await info_service.get_locations(city=city)

@router.get("/locations/{location_id}", response_model=CoffeeShopLocation)
async def read_location(
    location_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get information about a specific coffee shop location.
    """
    try:
        info_service = InfoService(db)
        return await info_service.get_location(location_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/locations", response_model=CoffeeShopLocation, status_code=status.HTTP_201_CREATED)
async def create_location(
    location_in: CoffeeShopLocationCreate,
    current_user: User = Depends(get_current_active_staff),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new coffee shop location (only for staff).
    """
    info_service = InfoService(db)
    return await info_service.create_location(location_in)

@router.put("/locations/{location_id}", response_model=CoffeeShopLocation)
async def update_location(
    location_id: int,
    location_in: CoffeeShopLocationUpdate,
    current_user: User = Depends(get_current_active_staff),
    db: AsyncSession = Depends(get_db)
):
    """
    Update information about a coffee shop location (only for staff).
    """
    try:
        info_service = InfoService(db)
        return await info_service.update_location(location_id, location_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# Static Information
@router.get("/static/{key}", response_model=StaticInfo)
async def read_static_info(
    key: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get static information by key.
    """
    try:
        info_service = InfoService(db)
        return await info_service.get_static_info(key)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/static", response_model=Dict[str, str])
async def read_all_static_info(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all static information.
    """
    info_service = InfoService(db)
    return await info_service.get_all_static_info()

@router.post("/static", response_model=StaticInfo, status_code=status.HTTP_201_CREATED)
async def create_static_info(
    info_in: StaticInfoCreate,
    current_user: User = Depends(get_current_active_staff),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new static information record (only for staff).
    """
    try:
        info_service = InfoService(db)
        return await info_service.create_static_info(info_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/static/{key}", response_model=StaticInfo)
async def update_static_info(
    key: str,
    info_in: StaticInfoUpdate,
    current_user: User = Depends(get_current_active_staff),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a static information record (only for staff).
    """
    try:
        info_service = InfoService(db)
        return await info_service.update_static_info(key, info_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# Company Information
@router.get("/company", response_model=CompanyInfo)
async def get_company_info(
    db: AsyncSession = Depends(get_db)
):
    """
    Get general information about the company.
    """
    info_service = InfoService(db)
    return await info_service.get_company_info()
