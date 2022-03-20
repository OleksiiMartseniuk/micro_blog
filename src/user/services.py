from fastapi import HTTPException

from google.oauth2 import id_token
from google.auth.transport import requests

from src.service_base import BaseService
from src.user import schemas, tokenizator
from src.user import models
from src.config.settings import GOOGLE_CLIENT_ID


class UserService(BaseService):
    model = models.User
    get_schema = schemas.GetUser


user_s = UserService()


async def create_user(user: schemas.UserCreate) -> models.User:
    _user, _ = await models.User.get_or_create(**user.dict(exclude={"token"}))
    return _user


async def google_auth(user: schemas.UserCreate) -> tuple:
    try:
        idinfo = id_token.verify_oauth2_token(user.token, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(403, "Bad code")
    user = await create_user(user)
    internal_token = tokenizator.create_token(user.id)
    return user.id, internal_token.get("access_token")
