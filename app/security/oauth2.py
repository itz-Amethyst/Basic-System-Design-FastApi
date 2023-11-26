from jose import JWTError , jwt
from jose.constants import ALGORITHMS
from datetime import datetime , timedelta
from app import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.shared import settings , errors

from app.security.TokenOperation import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')






def get_current_user(token: str = Depends(oauth2_scheme)):


    return verify_access_token(token , errors.credentials_exception)