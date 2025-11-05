# backend/main.py

from fastapi import FastAPI
from backend.database import create_db_and_tables
from backend.auth.routes import router as auth_router
from backend.todo.routes import router as todo_router

# create FastAPI app
app = FastAPI(title="Todo API with Auth")

# include routers
app.include_router(auth_router)
app.include_router(todo_router)

# create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# home route
@app.get("/")
def root():
    return {"message": "Welcome to the Todo API!"}
