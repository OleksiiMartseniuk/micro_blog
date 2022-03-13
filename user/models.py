from typing import Optional

from pydantic import BaseModel, EmailStr
from fastapi_users import models
from fastapi_users.db import TortoiseBaseUserModel
from tortoise.contrib.pydantic import PydanticModel
from tortoise import fields

from blog.models import Post


class User(models.BaseUser):
    username: str


class UserCreate(models.BaseUserCreate):
    username: str


class UserUpdate(models.BaseUserUpdate):
    username: Optional[str]


class UserModel(TortoiseBaseUserModel):
    username = fields.CharField(max_length=50, unique=True)
    posts: fields.ForeignKeyRelation[Post]


class UserDB(User, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = UserModel


class Status(BaseModel):
    message: str
