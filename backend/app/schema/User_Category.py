from pydantic import BaseModel

class UserCategorySchema(BaseModel):
    user_id: str
    category_id: str