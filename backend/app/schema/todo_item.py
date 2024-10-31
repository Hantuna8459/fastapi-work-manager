from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


class TodoItemBaseSchema(BaseModel):
    name: str
    description: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")

        if name == "":
            raise ValueError("Name can't be blank")

        return name

    @field_validator("description")
    @classmethod
    def validate_name(cls, description):
        if not isinstance(description, str):
            raise ValueError("Description must be a string")

        if description == "":
            raise ValueError("Description can't be blank")

        return description


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