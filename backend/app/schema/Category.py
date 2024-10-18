from datetime import datetime
from pydantic import BaseModel

from .Todo_item import TodoItemSchema


class CategoryCreateSchema(BaseModel):
    name: str
    description: str


class CategorySchema(CategoryCreateSchema):
    id: str
    created_by: str
    updated_at: datetime

class CategoryWithItemsSchema(CategorySchema):
    created_at: datetime
    todo_items: list[TodoItemSchema]