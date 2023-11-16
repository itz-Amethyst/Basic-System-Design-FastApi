from datetime import datetime

from sqlalchemy import Column , Integer , String , TIMESTAMP , ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.db.database import Base
from app.db.models.user import User

class Parent(Base):
    __tablename__ = 'Parents'

    id = Column(Integer , primary_key = True , nullable = False)
    title = Column(String , nullable = False)
    created_at = Column(TIMESTAMP(timezone = True) , nullable = False , server_default = text('now()') ,
                        default = datetime.now())
    owner_id = Column(String , ForeignKey(User.id , ondelete = "CASCADE") , nullable = False)

    owner = relationship(User)

