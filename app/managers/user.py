from fastapi import HTTPException, Request

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.db.models import User
from app.db.models.user import RoleOptions
from app.managers import PermissionManager
from app.managers.auth import AuthManager
from utils.AvatarUploadChunk import Upload_By_Chunk
from utils.Hashes import hash_password, verify_password
from app.schemas import UserRegister
from app.shared.errors import user_not_found , same_role

# Next should be added whenever you want to access db outside api
db: Session = next(get_db())

class UserManager:

    @staticmethod
    async def register(user_data: UserRegister, request: Request):
        if user_data.terms_of_service_accepted is False:
            raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE ,
                                detail = "You must agree terms of services")

        # Todo: Fix this later by adding default image
        if user_data.profile_picture is None:
            raise HTTPException(status_code = status.HTTP_411_LENGTH_REQUIRED ,
                                detail = "Please provide a profile picture")

        check_user = db.query(User).filter(User.email == user_data.email).first()

        if check_user:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT ,
                                detail = f"User with this email {user_data.email} already exists")

        mime , image_path , ext , filename = Upload_By_Chunk(request , user_data.profile_picture)

        password = hash_password(user_data.password.get_secret_value())

        new_user: User = User(email = user_data.email , password = password , image_path = image_path ,
                              size = user_data.profile_picture.size , ext = ext[1:] , mime = mime)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user



    @staticmethod
    def login(user_credentials: OAuth2PasswordRequestForm, request: Request):
        # It's not actually username it could be email either
        # Note .first() should be added
        user = db.query(User).filter(User.email == user_credentials.username).first()

        print(user)

        if not user:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = f"Invalid Credentials")

        if not verify_password(user_credentials.password , user.password):
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = f"Invalid Credentials")

        imp_data = {"id": user.id , "email": user.email , "role": user.role.value}

        # You can give role later or anything , scopes of access
        access_token = AuthManager.create_access_token(
            data = imp_data)

        PermissionManager.set_session_user(request = request , data = imp_data)

        return {"access_token": access_token , "token_type": "bearer"}


    @staticmethod
    def ChangeRole(user_id: str, role: RoleOptions):

        user = db.query(User).where(User.id == user_id).first()

        if user is None:
            raise user_not_found

        if user.role.value == role.value:
            raise same_role

        user.role = role.name
        db.commit()

        return user
