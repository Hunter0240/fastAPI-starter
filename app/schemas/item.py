from datetime import datetime

from pydantic import BaseModel


class ItemCreate(BaseModel):
    title: str
    description: str | None = None


class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class ItemResponse(BaseModel):
    id: str
    title: str
    description: str | None
    owner_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedItems(BaseModel):
    items: list[ItemResponse]
    total: int
    offset: int
    limit: int
