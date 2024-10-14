from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.exception import *
from backend.app.core.database import get_db
from backend.app.models import User
from backend.app.schema.UserRegisterSchema import UserRegister

def get_user(user_id: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()

def delete_user(user_id: str, db: Session = Depends(get_db)):
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if user_to_delete is None:
        return NoneDBException
    else:
        db.delete(user_to_delete)
        db.commit()

def register_user(user: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        return RegisterException
    user_register = User(username = user.username, password = user.password, email = user.email, last_name = user.last_name, first_name = user.first_name)
    db.add(user_register)
    db.commit()
    db.refresh(user_register)
    return {
        "new user": user.name,
        "id": user_register.id,
        "email": user.email,
        "first name": user.first_name,
        "last name": user.last_name
    }