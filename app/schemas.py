from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True



class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post : Post
    votes : int
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None    

class Vote(BaseModel):
    post_id:int
    dir: Literal[0,1]
