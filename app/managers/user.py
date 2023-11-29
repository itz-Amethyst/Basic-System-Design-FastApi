from http.client import HTTPException

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.db.models import User
from app.managers.auth import AuthManager
from utils.Hashes import hash_password, verify_password

# Next should be added whenever you want to access db outside api
db: Session = next(get_db())
class UserManager:

    @staticmethod
    async def register(user_data):
        pass



    @staticmethod
    async def login(user_credentials: OAuth2PasswordRequestForm):
        # It's not actually username it could be email either
        # Note .first() should be added
        user = await db.query(User).filter(User.email == user_credentials.username).first()

        print(user)

        if not user:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = f"Invalid Credentials")

        # TODO : FiX
        if not verify_password(user_credentials.password , user.password):
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = f"Invalid Credentials")

        # You can give role later or anything , scopes of access
        access_token = AuthManager.create_access_token(
            data = {"user_id": user.id , "user_email": user.email , "role": user.role.value})

        return {"access_token": access_token , "token_type": "bearer"}