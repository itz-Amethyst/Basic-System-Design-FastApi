from datetime import datetime , timedelta
from app import schemas
from typing import Optional
from jose import jwt , JWTError
from jose.constants import ALGORITHMS
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from starlette.requests import Request
from app.shared import settings , errors


class AuthManager:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()

        try:
            expire = datetime.utcnow() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"exp": expire})

            # ! By reading from algorithm class or directly by variable
            encoded_jwt = jwt.encode(to_encode , settings.SECRET_KEY , algorithm = ALGORITHMS.HS256)

            return encoded_jwt
        except Exception as e:
            raise e

    @staticmethod
    def verify_access_token( token: str , credentials_exception ):

        try:
            payload = jwt.decode(token , settings.SECRET_KEY , algorithms = [settings.ALGORITHM])

            user_id = payload.get("user_id")

            user_email = payload.get("user_email")

            role = payload.get("role")

            if user_id is None:
                raise credentials_exception

            token_data = schemas.TokenData(id = user_id , email = user_email , role = role)

        except JWTError:
            raise credentials_exception

        return token_data


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self , request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(res.credentials, settings.SECRET_KEY, algorithms = [ALGORITHMS.HS256])

            encoded_jwt = AuthManager.create_access_token(payload)

            result = AuthManager.verify_access_token(encoded_jwt, credentials_exception = errors.credentials_exception)

            request.state.user = result

            print(result)

            return result

        except JWTError:
            raise errors.credentials_exception