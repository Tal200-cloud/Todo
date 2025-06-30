import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base, engine, SessionLocal

# Define the Todo model
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create the database tables 
Base.metadata.create_all(bind=engine)


# FastAPI app
app = FastAPI()

#frontend port
origins = [
    "http://localhost:5173"
]


# security implementation, disallowing unauthorised acsess

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_headers = ["*"]

)

# Pydantic models implementation
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoResponse(TodoCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Dependency to get DB session implementation
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD functions implementation
def create_activity(db: Session, todo: TodoCreate):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).offset(skip).limit(limit).all()

def get_activity(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def update_activity(db: Session, todo_id: int, todo: TodoCreate):
    db_todo = get_activity(db, todo_id)
    if not db_todo:
        return None
    for field, value in todo.dict().items():
        setattr(db_todo, field, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = get_activity(db, todo_id)
    if not db_todo:
        return False
    db.delete(db_todo)
    db.commit()
    return True

# API endpoints implementation
@app.post("/todos/", response_model=TodoResponse)
def create_new_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_activity(db=db, todo=todo)

@app.get("/todos/", response_model=List[TodoResponse])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_activities(db, skip=skip, limit=limit)

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = get_activity(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_existing_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = update_activity(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_existing_todo(todo_id: int, db: Session = Depends(get_db)):
    if not delete_todo(db, todo_id=todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8000)