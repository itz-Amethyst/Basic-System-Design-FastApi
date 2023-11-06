from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None

# Huum maybe works
class CreatePost(Post):
    pass

class UpdatePost(Post):
    test: str

class PostView(Post):
    # Example
    # id : int
    created_at: datetime

    # Not necessary
    class Config:
        orm_mode = True

# @dataclass
# class Post:
#     title: str
#     content: str