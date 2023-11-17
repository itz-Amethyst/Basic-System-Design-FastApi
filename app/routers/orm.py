from typing import List

from fastapi import Depends , status , APIRouter , HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db
from app import schemas , oauth2

from app.db.models import Parent

router = APIRouter(
    prefix = '/orm',
    # You can add multiple tags
    tags = ['Orm']
)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create_table(data:schemas.Orm, db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    check_duplication = db.query(Parent).filter(Parent.title == data.title).first()

    if check_duplication:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT ,
                            detail = f"Table with this title {data.title} already exists")

    create_table_query = f"""CREATE TABLE {data.title} (id SERIAL PRIMARY KEY);"""
    db.execute(text(create_table_query))

    insert_parent = ("""INSERT INTO "Parents" (title,owner_id) VALUES (:title, :owner_id);""")

    db.execute(text(insert_parent), {"title": data.title, "owner_id": current_user.id})

    db.commit()

    # Todo: later implement schema to show the datas
    # res = Parent(owner_id = current_user.id, **data.dict())

    return {"Message": f"Table with id {data.title} Created !"}


@router.get('/', status_code = status.HTTP_201_CREATED, response_model = List[schemas.OrmView])
def get_tables(db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    tables = db.query(Parent).all()

    return tables