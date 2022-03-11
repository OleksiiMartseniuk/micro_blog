from typing import Optional

from pydantic import BaseModel
from fastapi_users import models
from fastapi_users.db import TortoiseBaseUserModel
from tortoise.contrib.pydantic import PydanticModel
from tortoise import fields

from blog.models import Post


class User(models.BaseUser):
    username: str
    avatar: Optional[str]


class UserCreate(models.BaseUserCreate):
    username: str
    avatar: Optional[str]


class UserUpdate(models.BaseUserUpdate):
    username: Optional[str]
    avatar: Optional[str]


class UserModel(TortoiseBaseUserModel):
    username = fields.CharField(max_length=50, unique=True)
    avatar = fields.CharField(max_length=200)
    posts: fields.ForeignKeyRelation[Post]


class UserDB(User, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = UserModel


class Status(BaseModel):
    message: str
