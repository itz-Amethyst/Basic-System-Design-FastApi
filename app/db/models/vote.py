from sqlalchemy import Column , Integer , String, ForeignKey
from app.db.database import Base


class Vote(Base):
    __tablename__ = "Votes"

    post_id = Column(Integer , ForeignKey("Posts.id" , ondelete = "CASCADE") , nullable = False, primary_key = True)
    user_id = Column(String , ForeignKey("Users.id" , ondelete = "CASCADE") , nullable = False, primary_key = True)