from typing import Optional
from pydantic import BaseModel, Field


class SearchParams(BaseModel):
    query: Optional[str] = Field(None, min_length=1)
    category_id: Optional[int] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    is_available: Optional[bool] = None


def get_search_params(
    query: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_available: Optional[bool] = None
) -> SearchParams:
    return SearchParams(
        query=query,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        is_available=is_available
    )
