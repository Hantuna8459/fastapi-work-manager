from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from models.Todo_Item import item_status

class TodoItemBase(BaseModel):
    name: str = Field(..., max_length = 25)
    description: str
    status: item_status = item_status.Todo

class TodoItemCreate(TodoItemBase):
    create_by: UUID
    category_id: Optional[UUID] = None

class TodoItemUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length = 25)
    description: Optional[str] = None
    status: Optional[item_status] = None

class TodoItemResponse(TodoItemBase):
    id: UUID

    class Config:
        orm_mode = True