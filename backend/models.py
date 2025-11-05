# backend/models.py

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


# -------------------------
# USER MODEL (DB TABLE)
# -------------------------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)        # auto generate id
    username: str = Field(index=True, nullable=False)                # username of user
    hashed_password: str                                             # store hashed password
    created_at: datetime = Field(default_factory=datetime.utcnow)    # signup time


# -------------------------
# TODO MODEL (DB TABLE)
# -------------------------
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)         # auto id
    title: str                                                        # todo title
    description: Optional[str] = None                                 # description optional
    completed: bool = Field(default=False)                            # default not done
    created_at: datetime = Field(default_factory=datetime.utcnow)     # created time
    owner_id: int = Field(foreign_key="user.id")                      # connected to user table


# -------------------------
# SCHEMAS (INPUT / OUTPUT)
# These are NOT database tables
# -------------------------

# Input when user creates todo
class TodoCreate(SQLModel):
    title: str
    description: Optional[str] = None

# Input when user updates todo
class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Output model for todo response
class TodoRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True    # important for SQLModel -> JSON


# -------------------------
# AUTH related SCHEMAS
# -------------------------
class UserCreate(SQLModel):
    username: str
    password: str

class UserRead(SQLModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

# token response
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
