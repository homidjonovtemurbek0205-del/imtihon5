from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.schemas.auth_schemas import LoginSchema, RegisterSchema


def create_user(data: RegisterSchema, db: Session):
    user = db.execute(select(User).where(User.email == data.email)).scalar_one_or_none()
    if user:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    user_data = data.model_dump()
    user_data["hashed_password"] = hash_password(user_data.pop("password"))
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def handle_login(data: LoginSchema, db: Session):
    user = db.execute(select(User).where(User.email == data.email)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Email or password is not correct")
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email or password is not correct")

    access_token_data = {"id": user.id}
    return {
        "access_token": create_access_token(access_token_data),
        "token_type": "bearer",
    }