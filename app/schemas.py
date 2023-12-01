from datetime import datetime
from typing import Optional

from fastapi import UploadFile , File
from pydantic import BaseModel , EmailStr , conint , SecretStr, Field
from app.db.models.parent import StatusOptions
from app.db.models.user import RoleOptions


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr

class UserRegister(UserLogin):
    terms_of_service_accepted: Optional[bool] = False
    profile_picture: UploadFile = File(...)


class UserUpdate(UserLogin):

    # you can put these in create option and inherit from them
    is_active : Optional[bool] = True
    is_superUser : Optional[bool] = False


#! Custom Way view
class UserView(BaseModel):
    id: str
    email: EmailStr
    password: SecretStr
    created_at: datetime
    role: RoleOptions
    image_path: str
    size: int
    ext: str
    mime: str
    image_path: Optional[str] = None
    terms_of_service: Optional[bool] = Field(default = False)


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
    role: Optional[str] = None



class Orm(BaseModel):
    title: str
    status: StatusOptions


class OrmView(Orm):
    id: int
    created_at: datetime
    owner_id: str
    owner: UserView


# @dataclass
# class Post:
#     title: str
#     content: str
