import os
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
try:
    from fastapi import Depends, HTTPException, status
    from fastapi.security import OAuth2PasswordBearer
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
except ImportError:
    Depends = HTTPException = status = oauth2_scheme = None
from .database import get_db
from .models import User
from .schemas import UserCreate, UserResponse, Token
SECRET_KEY = os.getenv("JWT_SECRET", "adaptprep_secret_key_for_placement_demo_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a hashed bcrypt password.
    Truncates password to 72 bytes as per bcrypt specification.
    """
    if not plain_password or not hashed_password:
        return False
    pwd_bytes = plain_password.encode('utf-8')[:72]
    try:
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode('utf-8'))
    except Exception:
        return False
def get_password_hash(password: str) -> str:
    """
    Generates a secure bcrypt hash for the given password.
    Truncates password to 72 bytes as per bcrypt specification.
    """
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')
