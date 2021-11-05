from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True

class UserOut(BaseModel) :
    id: int
    email:EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
class PostCreate(PostBase): 
    pass

class Post(PostBase):
    id:str
    created_at: datetime
    owner_id: str
    owner: UserOut
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional[str]= None

class Vote(BaseModel):
    post_id: int
    dir : conint(le=1)

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True