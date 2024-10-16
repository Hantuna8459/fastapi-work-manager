from backend.app.models.User import User
from backend.app.schema.user_schema import UserRegisterRequest
from backend.app.core.auth import get_hashed_password
from backend.app.core.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends

def register_request(*, session:Session = Depends(get_db), request:UserRegisterRequest)->User:
    new_user = User(
        email = request.email,
        username = request.username,
        password = get_hashed_password(request.password),
        is_active=True,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def get_user_by_email_or_username(*, session:Session = Depends(get_db), email:str, username:str)->User|None:
    """
    retrieve both email and username
    """
    statement = select(User).where(
            (User.email == email) | (User.username == username)
        )
    session_user = session.execute(statement).first()
    return session_user