# backend/auth/routes.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from backend.models import UserCreate, Token, User
from backend.database import get_session
from backend.auth.hashing import hash_password, verify_password
from backend.auth.jwt_handler import create_access_token, get_user_by_username

# router for auth endpoints
router = APIRouter(prefix="/auth", tags=["Auth"])


# ------------------------------
# SIGNUP ROUTE(create new user)
# ------------------------------
@router.post("/signup", response_model=Token)
def signup(user_in: UserCreate, session: Session = Depends(get_session)):

    # check if username already exists
    existing_user = get_user_by_username(session, user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # hash password
    password_str = str(user_in.password)[:72]   # ensure string + limit
    hashed_password_value = hash_password(password_str)

    # create new user
    new_user = User(username=user_in.username, hashed_password=hashed_password_value)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # create JWT token
    token = create_access_token({"sub": new_user.username})

    return {"access_token": token, "token_type": "bearer"}


# ------------------------------
# LOGIN ROUTE(generate token)
# ------------------------------
@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):

    # find user
    user = get_user_by_username(session, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # token
    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}
