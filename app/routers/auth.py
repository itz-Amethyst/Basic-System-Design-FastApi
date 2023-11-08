from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from utils.Hashes import verify_password
from .. import database, schemas, models

router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login")
def login(user_credentials: schemas.UserLogin ,db: Session = Depends(database.get_db)):

    user: models.User = db.query(models.User).get(models.User.email == user_credentials.email)

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid Credentials")

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid Credentials")