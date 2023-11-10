from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from utils.Hashes import verify_password
from app import database, schemas, models, oauth2

router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login", response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(database.get_db)):

    # It's not actually username it could be email either
    # Note .first() should be added
    user: models.User = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    print(user)

    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")

    # TODO : FiX
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")

    # You can give role later or anything , scopes of access
    access_token = oauth2.create_access_token(data = {"user_id": user.id, "user_email": user.email})

    return {"access_token" : access_token, "token_type": "bearer"}