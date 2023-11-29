from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from managers.user import UserManager
from app import schemas

router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login", response_model = schemas.Token)
async def login( user_credentials: OAuth2PasswordRequestForm = Depends()):

    return await UserManager.login(user_credentials)