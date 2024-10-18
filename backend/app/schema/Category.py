from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from .Todo_item import TodoItemSchema


class CategoryCreateSchema(BaseModel):
    name: str
    description: str


class CategorySchema(CategoryCreateSchema):
    id: UUID
    created_by: UUID
    updated_at: datetime

class CategoryWithItemsSchema(CategorySchema):
    created_at: datetime