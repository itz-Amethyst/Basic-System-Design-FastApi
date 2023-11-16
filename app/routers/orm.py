from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db
from utils.Hashes import hash_password
from app import schemas , oauth2

from app.db.models import User

router = APIRouter(
    prefix = '/orm',
    # You can add multiple tags
    tags = ['Orm']
)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create_user(data:schemas.Orm, db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    create_table_query = f"""CREATE TABLE {data.title} (id SERIAL PRIMARY KEY);"""
    db.execute(text(create_table_query))

    insert_parent = ("""INSERT INTO "Parents" (title,owner_id) VALUES (:title, :owner_id);""")

    db.execute(text(insert_parent), {"title": data.title, "owner_id": current_user.id})

    db.commit()

    return {"message": "successful"}