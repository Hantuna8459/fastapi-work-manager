from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from .todo_item import TodoItemSchema


class CategoryCreateSchema(BaseModel):
    name: str
    description: str


class CategorySchema(CategoryCreateSchema):
    id: UUID
    created_by: UUID
    updated_at: datetime | None

class CategoryWithItemsSchema(CategorySchema):
    created_at: datetime