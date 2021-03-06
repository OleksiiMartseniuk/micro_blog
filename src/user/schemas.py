from pydantic import EmailStr, BaseModel
from src.user import models
from tortoise.contrib.pydantic import pydantic_model_creator


GetUser = pydantic_model_creator(models.User, name="get_user")


class User(BaseModel):
    username: str
    email: EmailStr
    avatar: str


class UserCreate(User):
    token: str


class UserUpdate(User):
    pass


class UserOut(BaseModel):
    id: int
    username: str
    avatar: str


class Token(BaseModel):
    id: int
    token: str


class TokenPayload(BaseModel):
    user_id: int = None
