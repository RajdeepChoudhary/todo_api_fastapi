# backend/auth/jwt_handler.py

from typing import Optional, Dict
from datetime import datetime, timedelta

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select

from backend.models import User
from backend.database import get_session


# ------------------------------
# JWT CONFIG SETTINGS
# ------------------------------
SECRET_KEY = "change_this_secret_for_production"   # change later
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 12


# ------------------------------
# CUSTOM BEARER AUTH (no 'request' in Swagger)
# ------------------------------
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials or credentials.scheme.lower() != "bearer":
            raise HTTPException(status_code=403, detail="Invalid or missing token")
        return credentials.credentials

    # Hide "request" from Swagger (this is key)
    def __call_dependency__(self, request: Request):
        return super().__call__(request)


oauth2_scheme = JWTBearer()


# ------------------------------
# TOKEN CREATION
# ------------------------------
def create_access_token(data: Dict) -> str:
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ------------------------------
# FETCH USER BY USERNAME
# ------------------------------
def get_user_by_username(session: Session, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


# ------------------------------
# GET CURRENT USER FROM TOKEN
# ------------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(session, username)
    if user is None:
        raise credentials_exception

    return user
