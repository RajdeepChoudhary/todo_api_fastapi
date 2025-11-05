# backend/auth/jwt_handler.py

from typing import Optional, Dict
from datetime import datetime, timedelta

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from backend.models import User
from backend.database import get_session

# JWT config settings
SECRET_KEY = "change_this_secret_for_production"   # change later
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 12

# OAuth2 scheme (FastAPI extracts Bearer token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# create access token with expiry
def create_access_token(data: Dict) -> str:
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# helper to fetch user by username
def get_user_by_username(session: Session, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


# dependency: decode token -> return current user
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # get user record from DB
    user = get_user_by_username(session, username)
    if user is None:
        raise credentials_exception

    return user
