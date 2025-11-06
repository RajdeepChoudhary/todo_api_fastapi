# backend/main.py

from fastapi import FastAPI
from backend.database import create_db_and_tables
from backend.auth.routes import router as auth_router
from backend.todo.routes import router as todo_router
from fastapi import Depends
from backend.auth.jwt_handler import get_current_user
from backend.models import User

# create FastAPI app
app = FastAPI(title="Todo API with Auth")

# --- Add JWT security scheme to OpenAPI manually ---
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="Todo API with JWT Authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "JWTBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"JWTBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


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

@app.get("/whoami")
def whoami(current_user: User = Depends(get_current_user)):
    return {
        "logged_in_as": current_user.username,
        "user_id": current_user.id
    }
