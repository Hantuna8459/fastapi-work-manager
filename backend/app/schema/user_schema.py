from pydantic import EmailStr, Field, BaseModel
from typing import Optional

class UserResponse(BaseModel):
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    
    class Config:
        form_atrributes = True
    
class UserRegisterRequest(UserResponse):
    email:EmailStr
    password: str = Field(min_length=8, max_length=40)
    password_confirm: str = Field(min_length=8, max_length=40)
    username: str