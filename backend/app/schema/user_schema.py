import uuid
from datetime import datetime
from pydantic import EmailStr, Field, BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True
    
    class Config:
        form_atrributes = True

    
class UserRegisterRequest(UserBase):
    email:EmailStr
    password: str = Field(min_length=4, max_length=40)
    password_confirm: str = Field(min_length=4, max_length=40)
    username: str


class UserResponse(UserBase):
    id: uuid.UUID