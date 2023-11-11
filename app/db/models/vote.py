from sqlalchemy import Column , Integer , String, ForeignKey
from app.db.database import Base
from app.db.models.user import User
from app.db.models.post import Post


class Vote(Base):
    __tablename__ = "Votes"

    post_id = Column(Integer , ForeignKey(Post.id , ondelete = "CASCADE") , nullable = False, primary_key = True)
    user_id = Column(String , ForeignKey(User.id , ondelete = "CASCADE") , nullable = False, primary_key = True)