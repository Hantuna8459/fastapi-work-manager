from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TodoItemBaseSchema(BaseModel):
    name: str
    description: str
    category_id: UUID


class TodoItemSchema(TodoItemBaseSchema):
    id: UUID
    status: str
    created_by: UUID
    category_id: UUID | None = None


class TodoItemDeepSchema(TodoItemSchema):
    created_at: datetime
    updated_at: datetime | None