from fastapi import APIRouter, Depends
from app.dependencies.auth_dependencies import get_current_user
from app.dependencies.db_dependencies import get_db
from app.schemas.auth_schemas import CurrentUser, LoginResponse, LoginSchema, RegisterSchema, RegisterResponse
from app.services import auth_service, user_service

router = APIRouter()


@router.post("/auth/register", response_model=RegisterResponse)
def register(data: RegisterSchema, db=Depends(get_db)):
    return auth_service.create_user(data, db)


@router.post("/auth/login", response_model=LoginResponse)
def login(data: LoginSchema, db=Depends(get_db)):
    return auth_service.handle_login(data, db)


@router.get("/users/me", response_model=RegisterResponse)
def get_user_profile(current_user: CurrentUser = Depends(get_current_user), db=Depends(get_db)):
    return user_service.get_user_by_id(current_user.id, db)