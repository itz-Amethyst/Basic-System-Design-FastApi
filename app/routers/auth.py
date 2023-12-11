from fastapi import APIRouter, Depends, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.deps import rate_limit
from app.managers.user import UserManager
from app import schemas

router = APIRouter(
    tags = ['Authentication'],
    dependencies = [rate_limit('auth' , 30 * 60 , 20 , False)]
)

@router.post("/login", response_model = schemas.Token)
def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends()):

    return UserManager.login(user_credentials, request)