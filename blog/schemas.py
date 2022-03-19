from pydantic import BaseModel, EmailStr
from blog import models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Optional


GetPost = pydantic_model_creator(models.Post, name="get_post")
GetComment = pydantic_model_creator(models.Comment, name="get_comment")
GetTag = pydantic_model_creator(models.Tag, name="get_tag")


class CreatePost(BaseModel):
    title: str
    body: str
    image: Optional[str] = None


class UpdatePost(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    image: Optional[str] = None


class CreateComment(BaseModel):
    post_id: int
    name: str
    email: EmailStr
    body: str


class CreateTag(BaseModel):
    name: str


class Status(BaseModel):
    message: str
