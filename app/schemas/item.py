from typing import Optional
from datetime import datetime
from pydantic import BaseModel,Field,Schema


class ItemBase(BaseModel):
    title: str = Field(..., min_length=6, max_length=64)
    description: str = Field(..., min_length=6, max_length=128)


    class Config:
        schema_extra = {
            "example": {
                "title": "this is title",
                "description": "this is description"
            }
        }


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemInDB(ItemBase):
    id: int
    owner_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True
