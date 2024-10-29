import uuid
from datetime import datetime
from pydantic import EmailStr, Field, BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str] 
    
    class Config:
        form_atrributes = True

  
class UserRegisterRequest(BaseModel):
    email:EmailStr
    username: str
    password: str = Field(min_length=4, max_length=40)
    password_confirm: str = Field(min_length=4, max_length=40)

class UserUpdateRequest(BaseModel):
    username: str
    first_name: str
    last_name: str

class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=4, max_length=40)
    new_password: str = Field(min_length=4, max_length=40)

class UserResponse(UserBase):
    id: uuid.UUID
    
class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)