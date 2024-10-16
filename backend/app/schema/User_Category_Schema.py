from pydantic import BaseModel
from uuid import UUID

class UserCategoryBase(BaseModel):
    user_id: UUID
    category_id: UUID

class UserCategoryCreate(UserCategoryBase):
    pass