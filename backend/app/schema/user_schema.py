import uuid
from pydantic import EmailStr, Field, BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    
    class Config:
        from_attributes = True
    
class UserRegisterRequest(UserBase):
    email:EmailStr
    password: str = Field(min_length=8, max_length=40)
    password_confirm: str = Field(min_length=8, max_length=40)
    username: str


# class UserResponse(UserBase):
#     id: uuid.UUID