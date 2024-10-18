from datetime import datetime

from pydantic import BaseModel


class TodoItemBaseSchema(BaseModel):
    name: str
    description: str


class TodoItemCreateSchema(TodoItemBaseSchema):
    category_id: str | None = None


class TodoItemSchema(TodoItemBaseSchema):
    id: str
    status: str
    created_by: str
    category_id: str | None = None


class TodoItemDeepSchema(TodoItemSchema):
    created_at: datetime
    updated_at: datetime