from uuid import UUID
from datetime import datetime
from pydantic import EmailStr, Field, BaseModel

class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str|None = None
    last_name: str|None = None
    is_active: bool = True
    
    class Config:
        from_atrributes = True

    
class UserRegisterRequest(UserBase):
    email:EmailStr
    password: str = Field(min_length=4, max_length=40)
    password_confirm: str = Field(min_length=4, max_length=40)
    username: str


class UserResponse(UserBase):
    id: UUID
    last_login: datetime|None
