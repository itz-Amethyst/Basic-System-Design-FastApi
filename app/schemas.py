from datetime import datetime
from typing import Optional
from pydantic import BaseModel , EmailStr , conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserView(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime
    image_path: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


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
    owner_id: str
    owner: UserView

    # Not necessary
    class Config:
        from_attributes = True


# For Join  => view
# When ever it gets error try to makes it lowercase or restart the server
class PostViewWithVotes(BaseModel):
    Post: PostView
    votes: int

    class Config:
        from_attributes = True
        orm_mode = True


class Vote(BaseModel):
    post_id : int
    # less than equal 1
    # be 0 or 1 if 1 => create otherwise 0 => delete
    dir: conint(le = 1)



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None



class Orm(BaseModel):
    title: str


class OrmView(Orm):
    id: int
    created_at: datetime
    owner_id: str
    owner: UserView


# @dataclass
# class Post:
#     title: str
#     content: str
