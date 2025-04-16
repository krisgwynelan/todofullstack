from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models
from . import crud
from . import schemas
from . database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/todos", response_model=list[schemas.ToDoOut])
def read_todos(db: Session = Depends(get_db)):
    return crud.get_all_todos(db)

@app.post("/todos", response_model=schemas.ToDoOut)
def create(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@app.put("/todos/{todo_id}", response_model=schemas.ToDoOut)
def update(todo_id: int, todo: schemas.ToDoUpdate, db: Session = Depends(get_db)):
    return crud.update_todo(db, todo_id, todo)

@app.delete("/todos/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db, todo_id)

@app.get("/todos/filter/{status}", response_model=list[schemas.ToDoOut])
def filter_by_status(status: str, db: Session = Depends(get_db)):
    todos = crud.get_all_todos(db)
    if status == "completed":
        return [t for t in todos if t.completed]
    elif status == "pending":
        return [t for t in todos if not t.completed]
    return todos
