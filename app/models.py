from datetime import datetime

from sqlalchemy import Column , Integer , String , Boolean , TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String(250), nullable = False)
    published = Column(Boolean, nullable = False, server_default = "False")
    rating = Column(Integer, nullable = False,)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'), default = datetime.now())
