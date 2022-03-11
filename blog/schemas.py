from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from blog import models

from pydantic import BaseModel, EmailStr
from typing import Optional


GetPost = pydantic_model_creator(models.Post, name="get_post")
GetComment = pydantic_model_creator(models.Comment, name="get_comment")


class CreatePost(PydanticModel):
    title: str
    body: str


class UpdatePost(PydanticModel):
    title: Optional[str] = None
    body: Optional[str] = None


class CreateComment(PydanticModel):
    post_id: int
    name: str
    email: EmailStr
    body: str


class Status(BaseModel):
    message: str
