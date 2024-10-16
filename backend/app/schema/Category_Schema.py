from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class CategoryBase(BaseModel):
    name: str = Field(..., max_length = 25)
    description: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length = 25)
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: UUID

    class Config:
        orm_mode = True