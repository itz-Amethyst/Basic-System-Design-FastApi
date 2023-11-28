from datetime import datetime , timedelta

from jose import jwt , JWTError
from jose.constants import ALGORITHMS

from app import schemas
from app.shared import settings


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

        role = payload.get("role")

        if user_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id = user_id, email = user_email, role = role)

    except JWTError:
        raise credentials_exception

    return token_data