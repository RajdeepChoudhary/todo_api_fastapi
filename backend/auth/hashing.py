# backend/auth/hashing.py

from passlib.context import CryptContext

# bcrypt hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash plain text password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# verify password during login
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
