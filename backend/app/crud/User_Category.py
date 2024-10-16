from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from models.User_Category import User_Category
from uuid import UUID

def create_user_category(user_id: UUID, category_id: UUID, db: Session = Depends(get_db)):
    stmt = User_Category.insert().values(user_id=user_id, category_id=category_id)
    db.execute(stmt)
    db.commit()
    return {
        "user_id: ": user_id,
        "category_id: ": category_id
    }

def delete_user_category(user_id: UUID, category_id: UUID, db: Session = Depends(get_db)):
    stmt = User_Category.delete().where(
        (User_Category.c.user_id == user_id) & (User_Category.c.category_id == category_id)
    )
    db.execute(stmt)
    db.commit()

def get_user_category(user_id: UUID, db: Session = Depends(get_db)):
    stmt = User_Category.select().where(User_Category.c.user_id == user_id)
    return db.execute(stmt).fetchall()

def get_category_user(category_id: UUID, db: Session = Depends(get_db)):
    stmt = User_Category.select().where(User_Category.c.category_id == category_id)
    return db.execute(stmt).fetchall()
