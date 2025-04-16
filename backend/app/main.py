from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models
from . import crud
from . import schemas
from .database import SessionLocal, engine, Base

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for localhost (React frontend) and GitHub Pages
origins = ["http://localhost:3000",
           "https://krisgwynelan.github.io", 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root route (optional, for testing purposes)
@app.get("/")
def read_root():
    return {"message": "Welcome to the ToDo API!"}

# Read all todos
@app.get("/todos", response_model=list[schemas.ToDoOut])
def read_todos(db: Session = Depends(get_db)):
    return crud.get_all_todos(db)

# Create a new todo
@app.post("/todos", response_model=schemas.ToDoOut)
def create(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

# Update an existing todo
@app.put("/todos/{todo_id}", response_model=schemas.ToDoOut)
def update(todo_id: int, todo: schemas.ToDoUpdate, db: Session = Depends(get_db)):
    return crud.update_todo(db, todo_id, todo)

# Delete a todo by ID
@app.delete("/todos/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    crud.delete_todo(db, todo_id)
    return {"message": f"Todo with ID {todo_id} deleted successfully."}

# Filter todos by status (completed or pending)
@app.get("/todos/filter/{status}", response_model=list[schemas.ToDoOut])
def filter_by_status(status: str, db: Session = Depends(get_db)):
    if status not in ["completed", "pending"]:
        raise HTTPException(status_code=400, detail="Invalid status. Use 'completed' or 'pending'.")
    
    # Query the database to filter based on status
    if status == "completed":
        return crud.get_todos_by_status(db, completed=True)
    elif status == "pending":
        return crud.get_todos_by_status(db, completed=False)

# CRUD methods for ToDo operations (could be in crud.py)

def get_all_todos(db: Session):
    return db.query(models.ToDo).all()

def create_todo(db: Session, todo: schemas.ToDoCreate):
    db_todo = models.ToDo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo: schemas.ToDoUpdate):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()

def get_todos_by_status(db: Session, completed: bool):
    return db.query(models.ToDo).filter(models.ToDo.completed == completed).all()
