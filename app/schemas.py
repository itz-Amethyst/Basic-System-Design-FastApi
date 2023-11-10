from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


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
    owner_id : str


    # Not necessary
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password:str

class UserView(BaseModel):
    id : str
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None
    email: EmailStr


# @dataclass
# class Post:
#     title: str
#     content: str