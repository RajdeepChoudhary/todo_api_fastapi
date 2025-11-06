# backend/todo/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.models import Todo, TodoCreate, TodoUpdate, TodoRead, User
from backend.database import get_session
from backend.auth.jwt_handler import get_current_user

router = APIRouter(prefix="/todos", tags=["Todos"])


# ------------------------------
# CREATE TODO (only logged in user)
# ------------------------------
@router.post("/", response_model=TodoRead)
def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        owner_id=current_user.id
    )
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo


# ------------------------------
# GET ALL TODOS for current user
# ------------------------------
@router.get("/", response_model=list[TodoRead])
def list_todos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(Todo.owner_id == current_user.id)
    todos = session.exec(statement).all()
    return todos


# ------------------------------
# GET SINGLE TODO by ID
# ------------------------------
@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = session.get(Todo, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# ------------------------------
# UPDATE TODO
# ------------------------------
@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = session.get(Todo, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    for field, value in todo_data.dict(exclude_unset=True).items():
        setattr(todo, field, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


# ------------------------------
# DELETE TODO
# ------------------------------
@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo = session.get(Todo, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo)
    session.commit()
    return {"message": f"Todo {todo_id} deleted successfully"}
