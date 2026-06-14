from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import verify_token
from app.schemas.auth_schemas import CurrentUser

security_header = HTTPBearer()


def get_current_user(token_data: HTTPAuthorizationCredentials = Depends(security_header)):
    token = token_data.credentials
    data = verify_token(token)
    if data is None:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")

    return CurrentUser.model_validate(data)