from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from models.Todo_Item import Todo_Item, item_status
from schema.TodoItem_Schema import TodoItemCreate, TodoItemUpdate
from uuid import UUID

def get_todo_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Todo_Item).offset(skip).limit(limit).all()

def get_todo_item(todo_id: UUID, db: Session = Depends(get_db)):
    return db.query(Todo_Item).filter(Todo_Item.id == todo_id).first()

def create_todo_item(todo: TodoItemCreate, db: Session = Depends(get_db)):
    db_todo = Todo_Item(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo_item(todo: TodoItemUpdate, todo_id: UUID, db: Session = Depends(get_db)):
    db_todo = db.query(Todo_Item).filter(Todo_Item.id == todo_id).first()
    if db_todo:
        for key, value in todo.dict(exclude_unset = True).items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo_item(todo_id: UUID, db: Session = Depends(get_db)):
    db_todo = db.query(Todo_Item).filter(Todo_Item.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo