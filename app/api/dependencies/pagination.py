from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    size: int
    pages: int


def get_pagination_params(
    page: int = 1,
    size: int = 10
) -> PaginationParams:
    return PaginationParams(page=page, size=size)
