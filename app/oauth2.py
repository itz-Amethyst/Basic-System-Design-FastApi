from jose import JWTError , jwt
from jose.constants import ALGORITHMS
from datetime import datetime , timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from shared import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES )
    to_encode.update({"exp": expire})

    # ! By reading from algorithm class or directly by variable
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm = ALGORITHMS.HS256)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token , settings.SECRET_KEY , algorithms = [settings.ALGORITHM])

        user_id = payload.get("user_id")

        user_email = payload.get("user_email")

        if user_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id = user_id, email = user_email)

    except JWTError:
        raise credentials_exception

    return token_data



def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})

    return verify_access_token(token , credentials_exception)