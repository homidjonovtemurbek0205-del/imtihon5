from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: int


class RegisterSchema(BaseModel):
    email: str
    password: str


class RegisterResponse(BaseModel):
    id: int
    email: str


class LoginSchema(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"