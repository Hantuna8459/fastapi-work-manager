import re
from uuid import UUID
from pydantic import EmailStr, Field, BaseModel, field_validator

class UserBase(BaseModel):
    email: EmailStr
    username: str
    
class UserPrivate(BaseModel):
    id: UUID
    password: str
    is_active: bool

class UserRegisterRequest(BaseModel):
    email:EmailStr
    username: str = Field(min_length=1, max_length=40)
    password: str = Field(min_length=8, max_length=40)
    password_confirm: str = Field(min_length=8, max_length=40)

class UsernameUpdateRequest(BaseModel):
    username: str = Field(min_length=1, max_length=40)


class FullnameUpdateRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)

class UserUpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)
    password_confirm: str = Field(min_length=8, max_length=40)

    @field_validator("new_password")
    def validate_password(cls, value):
        if not re.search(r"[a-zA-Z]",value):
            raise ValueError("Password must contain at least one character.")
        if not re.search(r"[0-9]",value):
            raise ValueError("Password must contain at least one number.")
        return value

class UserResponse(UserBase):
    id: UUID

class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class Deactivate(BaseModel):
    is_active: bool = False