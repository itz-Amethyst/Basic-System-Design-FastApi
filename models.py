from typing import Optional

from pydantic import BaseModel
from dataclasses import dataclass

class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None

# @dataclass
# class Post:
#     title: str
#     content: str