from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
