from pydantic import BaseModel
from uuid import UUID

class UserCategorySchema(BaseModel):
    user_ids: list[UUID]
    category_id: UUID