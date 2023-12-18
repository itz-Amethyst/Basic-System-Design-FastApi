from typing import List

from fastapi import Depends , status , APIRouter , HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db
from app import schemas

from app.db.models import Parent

from app.managers.permission import PermissionManager
from app.managers.auth import oauth2_bearer_schema
from Perseus import cache

router = APIRouter(
    prefix = '/orm',
    # You can add multiple tags
    tags = ['Orm']
)

@router.post('/', status_code = status.HTTP_201_CREATED)
def create_table(data:schemas.Orm, db: Session = Depends(get_db)):
    check_duplication = db.query(Parent).filter(Parent.title == data.title).first()

    if check_duplication:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT ,
                            detail = f"Table with this title {data.title} already exists")

    create_table_query = f"""CREATE TABLE {data.title} (id SERIAL PRIMARY KEY);"""
    db.execute(text(create_table_query))

    insert_parent = ("""INSERT INTO "Parents" (title,owner_id) VALUES (:title, :owner_id, :Status);""")

    db.execute(text(insert_parent), {"title": data.title, "owner_id": "24", "category": data.status})

    db.commit()

    # Todo: later implement schema to show the datas
    # res = Parent(owner_id = current_user.id, **data.dict())

    return {"Message": f"Table with id {data.title} Created !"}


# You can use both option to check dependencies
@router.get('/', status_code = status.HTTP_201_CREATED, response_model = List[schemas.OrmView], dependencies = [Depends(oauth2_bearer_schema), Depends(PermissionManager.is_admin)])
@cache(expire = 50)
def get_tables(db:Session = Depends(get_db)):

    tables = db.query(Parent).all()

    return tables