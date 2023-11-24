from fastapi import Depends , HTTPException , status , APIRouter , UploadFile , File , Request , Form
from pydantic import SecretStr , EmailStr
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.shared import settings
from utils.Hashes import hash_password
from app import schemas

from app.db.models import User
from utils.AvatarUploadChunk import Upload_By_Chunk


router = APIRouter(
    prefix = '/user',
    # You can add multiple tags
    tags = ['Users']
)

@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.UserView)
def create_user(request: Request, email: EmailStr = Form(),
    password: SecretStr = Form(),
    # is_superuser: bool = Form(),
    terms_of_service_accepted: bool = Form(),
    profile_picture: UploadFile = File(...) , db: Session = Depends(get_db)):


    if terms_of_service_accepted is False:
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE, detail = "You must agree terms of services")


    # Todo: Fix this later by adding default image
    if profile_picture is None:
        raise HTTPException(status_code = status.HTTP_411_LENGTH_REQUIRED, detail = "Please provide a profile picture")

    mime, image_path, ext, filename  = Upload_By_Chunk(request, profile_picture)

    check_user = db.query(User).filter(User.email == email).first()

    if check_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"User with this email {email} already exists")


    password = hash_password(password.get_secret_value())


    new_user: User = User(email = email, password = password, image_path = image_path, size = profile_picture.size, ext = ext[1:], mime = mime)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model = schemas.UserView)
def get_user(id: str, db: Session = Depends(get_db)):

    user = db.query(User).get(id)

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with this id {id} does not exists")

    return user