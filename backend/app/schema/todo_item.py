from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TodoItemBaseSchema(BaseModel):
    name: str
    description: str


class TodoItemWithCategorySchema(TodoItemBaseSchema):
    category_id: UUID


class TodoItemSchema(TodoItemBaseSchema):
    id: UUID
    status: str
    category_id: UUID
    created_by: UUID


class TodoItemDeepSchema(TodoItemSchema):
    created_at: datetime
    updated_at: datetime | None