from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from models.Category import Category
from schema.Category_Schema import CategoryCreate, CategoryUpdate
from uuid import UUID

def get_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Category).offset(skip).limit(limit).all()

def get_category(category_id: UUID, db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.id == category_id).first()

def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(category_id: UUID, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        for key, value in category.dict(exclude_unset = True).items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category