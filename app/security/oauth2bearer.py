from typing import Optional
from jose import jwt , JWTError
from jose.constants import ALGORITHMS

from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.db.database import get_db
from app.shared import settings , errors

from app.security.TokenOperation import create_access_token, verify_access_token


# Next should be added whenever you want to access db outside api
db: Session = next(get_db())

class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self , request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(res.credentials, settings.SECRET_KEY, algorithms = [ALGORITHMS.HS256])

            encoded_jwt = create_access_token(payload)

            result = verify_access_token(encoded_jwt, credentials_exception = errors.credentials_exception)

            request.state.user = result

            print(result)

            return result

        except JWTError:
            raise errors.credentials_exception


oauth2_schema_bearer = CustomHTTPBearer()