from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.hash import argon2

from app.core.config import settings


def hash_password(plain_password):
    return argon2.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return argon2.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta( minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    to_encode["type"] = "ACCESS_TOKEN"
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)


def create_refresh_token(user_id: int):
    to_encode = {"user_id": user_id}
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode["exp"] = expire
    to_encode["type"] = "REFRESH_TOKEN"
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        return payload
    except JWTError:
        return None