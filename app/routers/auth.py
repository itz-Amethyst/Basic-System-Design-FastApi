from fastapi import APIRouter, Depends, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.managers.user import UserManager
from app import schemas

router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login", response_model = schemas.Token)
def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends()):

    return UserManager.login(user_credentials, request)