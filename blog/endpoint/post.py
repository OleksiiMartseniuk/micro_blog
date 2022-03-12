from fastapi import Depends, APIRouter

from tortoise.contrib.fastapi import HTTPNotFoundError

from user.settings import current_active_user
from user.models import UserDB
from blog import schemas
from blog import service


post_router = APIRouter()


@post_router.get('/{pk}', response_model=schemas.GetPost, responses={404: {'model': HTTPNotFoundError}})
async def get_post(pk: int):
    return await service.post_s.get(id=pk)


@post_router.post('/', response_model=schemas.GetPost)
async def create_post(post: schemas.CreatePost, user: UserDB = Depends(current_active_user)):
    return await service.post_s.create(post, author_id=user.id)


@post_router.put('/{pk}', response_model=schemas.GetPost, responses={404: {'model': HTTPNotFoundError}})
async def update_post(pk: int, post: schemas.UpdatePost, user: UserDB = Depends(current_active_user)):
    return await service.post_s.update(post, id=pk, author_id=user.id)


@post_router.delete('/{pk}', response_model=schemas.Status, responses={404: {'model': HTTPNotFoundError}})
async def delete_post(pk: int, user: UserDB = Depends(current_active_user)):
    return await service.post_s.delete(id=pk, author_id=user.id)
