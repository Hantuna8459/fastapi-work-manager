from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, field_validator

from .todo_item import TodoItemSchema


class CategoryCreateSchema(BaseModel):
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


class CategorySchema(CategoryCreateSchema):
    id: UUID
    created_by: UUID
    updated_at: datetime | None

class CategoryWithItemsSchema(CategorySchema):
    created_at: datetime