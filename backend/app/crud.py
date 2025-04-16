from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models
from . import schemas

def get_all_todos(db: Session):
    return db.query(models.ToDo).all()

def get_todo(db: Session, todo_id: int):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

def create_todo(db: Session, todo: schemas.ToDoCreate):
    db_todo = models.ToDo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo: schemas.ToDoUpdate):
    db_todo = get_todo(db, todo_id)
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    db.delete(db_todo)
    db.commit()
    return {"message": f"Todo with ID {todo_id} deleted successfully."}

def get_todos_by_status(db: Session, completed: bool):
    return db.query(models.ToDo).filter(models.ToDo.completed == completed).all()
