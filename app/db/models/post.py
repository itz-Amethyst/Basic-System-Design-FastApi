
from datetime import datetime

from sqlalchemy import Column , Integer , String , Boolean , TIMESTAMP , ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.db.database import Base

class Post(Base):
    __tablename__ = 'Posts'

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String(250), nullable = False)
    published = Column(Boolean, nullable = False, server_default = "False")
    rating = Column(Integer, nullable = False,)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'), default = datetime.now())
    owner_id = Column(String, ForeignKey("Users.id", ondelete = "CASCADE"), nullable = False)

    owner = relationship("User")
