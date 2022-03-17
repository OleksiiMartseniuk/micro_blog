from fastapi import Depends, APIRouter, Request
from starlette.templating import Jinja2Templates
from user import schemas, services


templates = Jinja2Templates(directory='templates')


user_router = APIRouter()


@user_router.get('/')
async def google_auth(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})


@user_router.post('/google/auth', response_model=schemas.Token)
async def google_auth(user: schemas.UserCreate):
    user_id, token = await services.google_auth(user)
    return schemas.Token(id=user_id, token=token)
