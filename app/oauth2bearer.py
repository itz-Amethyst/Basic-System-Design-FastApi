from typing import Optional
import jwt
from fastapi import Depends
from jose.constants import ALGORITHMS

from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.db.database import get_db
from app.db.models import User
from app.shared import settings , errors


# Next should be added whenever you want to access db outside api
db: Session = next(get_db())

class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self , request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(res.credentials, settings.SECRET_KEY, algorithms = [ALGORITHMS.HS256])

            user =  db.query(User).where(User.id == payload['sub'])
            request.state.user = user
            return payload

        except jwt.ExpiredSignatureError:
            raise errors.credentials_exception

        except jwt.InvalidTokenError:
            raise errors.credentials_exception


oauth2_schema_bearer = CustomHTTPBearer()