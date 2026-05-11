from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
import uuid

from app.auth import (
    verify_password,
    create_access_token,
    get_current_user,
    fake_users_db,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

app = FastAPI(title="Task Management API")

# In-memory task store
tasks: dict[str, dict] = {}


class LoginRequest(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post("/login", response_model=Token)
def login(credentials: LoginRequest):
    user = fake_users_db.get(credentials.username)
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(
        data={"sub": credentials.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/tasks")
def get_tasks(current_user: str = Depends(get_current_user)):
    return list(tasks.values())


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate, current_user: str = Depends(get_current_user)):
    task_id = str(uuid.uuid4())
    new_task = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "completed": False,
        "owner": current_user,
    }
    tasks[task_id] = new_task
    return new_task


@app.put("/tasks/{task_id}")
def update_task(
    task_id: str, task: TaskUpdate, current_user: str = Depends(get_current_user)
):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    existing = tasks[task_id]
    if task.title is not None:
        existing["title"] = task.title
    if task.description is not None:
        existing["description"] = task.description
    if task.completed is not None:
        existing["completed"] = task.completed
    return existing


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str, current_user: str = Depends(get_current_user)):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
