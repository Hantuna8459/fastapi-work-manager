from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TodoItemBaseSchema(BaseModel):
    name: str
    description: str


class TodoItemCreateSchema(TodoItemBaseSchema):
    category_id: UUID | None


class TodoItemSchema(TodoItemBaseSchema):
    id: UUID
    status: str
    created_by: UUID
    category_id: UUID | None = None


class TodoItemDeepSchema(TodoItemSchema):
    created_at: datetime
    updated_at: datetime