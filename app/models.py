
from datetime import datetime

from sqlalchemy import Column , Integer , String , Boolean , TIMESTAMP
from sqlalchemy.sql.expression import text, func
from app.database import Base
from utils.CustomMethods import generate_generic_id


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String(250), nullable = False)
    published = Column(Boolean, nullable = False, server_default = "False")
    rating = Column(Integer, nullable = False,)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'), default = datetime.now())





class User(Base):
    __tablename__ = 'Users'

    #! Imp Note: It's not set on server default in db so whenever you create a custom data in db  dont except to auto generate id
    id = Column(String, primary_key = True, nullable = False, unique = True, default = generate_generic_id)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'), default = datetime.now())


