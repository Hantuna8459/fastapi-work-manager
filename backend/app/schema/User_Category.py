from pydantic import BaseModel
from uuid import UUID

class UserCategorySchema(BaseModel):
    user_id: UUID
    category_id: UUID