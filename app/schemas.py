from datetime import datetime
from typing import Optional
from pydantic import BaseModel , EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserView(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime


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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None

# @dataclass
# class Post:
#     title: str
#     content: str
