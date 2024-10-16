from backend.app.models.User import User
from backend.app.schema.user_schema import UserCreate
from backend.app.core.auth import get_hashed_password
from sqlalchemy import select
from sqlalchemy.orm import Session

def user_create(*, session:Session, user_create:UserCreate)->User:
    user_data = User(
        user_create,
        update = {"password":get_hashed_password(user_create.password)}
    )
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data

def get_user_by_email_or_username(*, session:Session, email:str, username:str)->User|None:
    """
    retrieve both email and username
    """
    statement = select(User).where(
            (User.email == email) & (User.username == username)
        )
    session_user = session.execute(statement).first()
    return session_user