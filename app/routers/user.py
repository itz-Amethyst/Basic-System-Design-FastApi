from fastapi import Depends , HTTPException , status , APIRouter , UploadFile , File , Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from utils.Hashes import hash_password
from app import schemas

from app.db.models import User
from utils.AvatarUploadChunk import Upload_By_Chunk


router = APIRouter(
    prefix = '/user',
    # You can add multiple tags
    tags = ['Users']
)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), file: UploadFile = File()):
    # user: User = request.state

    mime, path, ext, filename  = Upload_By_Chunk(file)

    check_user = db.query(User).filter(User.email == user.email).first()

    if check_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"User with this email {user.email} already exists")


    user.password = hash_password(user.password)
    new_user: User = User(**user.dict(), image_path = path, size = file.size, ext = ext[1:], mime = mime, filename = filename)
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "ok"}


@router.get('/{id}', response_model = schemas.UserView)
def get_user(id: str, db: Session = Depends(get_db)):

    user = db.query(User).get(id)

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with this id {id} does not exists")

    return user