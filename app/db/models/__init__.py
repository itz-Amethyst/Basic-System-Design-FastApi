from .post import Post
from .user import User
from .vote import Vote
from app.db.database import MetaData
from sqlalchemy import MetaData


# metadata = MetaData()
# metadata.create_all(bind = engine)


__all__ = [
    'Post', 'Vote', 'User',

    'MetaData'
]