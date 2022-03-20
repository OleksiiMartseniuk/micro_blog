from fastapi import Depends, APIRouter, Request
from starlette.templating import Jinja2Templates

from tortoise.contrib.fastapi import HTTPNotFoundError

from src.user import schemas
from src.user import services, models
from src.user.auth import get_user


templates = Jinja2Templates(directory='templates')


user_router = APIRouter()


@user_router.get('/')
async def google_auth(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})


@user_router.post('/google/auth', response_model=schemas.Token)
async def google_auth(user: schemas.UserCreate):
    user_id, token = await services.google_auth(user)
    return schemas.Token(id=user_id, token=token)


@user_router.get('/user/me', response_model=schemas.GetUser, responses={404: {"model": HTTPNotFoundError}})
async def get_user(user: models.User = Depends(get_user)):
    return await services.user_s.get(id=user.id)
