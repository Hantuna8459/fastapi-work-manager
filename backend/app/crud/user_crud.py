from backend.app.models.User import User
from backend.app.schema.user_schema import UserRegisterRequest
from backend.app.core.auth import get_hashed_password
from backend.app.core.database import get_db
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import Depends
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_by_email_or_username(*, session:Session = Depends(get_db), email:str, username:str)->User|None:
    """
    retrieve both email and username
    """
    try:
        statement = select(User).where(
                (User.email == email) | (User.username == username)
            )
        session_user = session.execute(statement).first()
        return session_user
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error occurred while querying user by email or username: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None

def get_user_by_id(*, session:Session = Depends(get_db), id:uuid.UUID)->User|None:
    try:
        statement = select(User).where(User.id == id)
        session_user = session.execute(statement).first()
        return session_user
    except SQLAlchemyError as e:
        session.rollback()
        return None

def register_request(*, session:Session = Depends(get_db), request:UserRegisterRequest)->User:
    new_user = User(
        email = request.email,
        username = request.username,
        password = get_hashed_password(request.password),
        is_active=True,
    )
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"SQLAlchemy error occurred: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None