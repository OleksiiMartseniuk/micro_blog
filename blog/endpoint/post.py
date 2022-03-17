from fastapi import Depends, APIRouter

from user.auth import get_user
from user.models import User
from blog import schemas, service
from tortoise.contrib.fastapi import HTTPNotFoundError


post_router = APIRouter()


@post_router.get('/{pk}', response_model=schemas.GetPost)
async def get_post(pk: int):
    return await service.post_s.get(id=pk)


@post_router.post('/', response_model=schemas.GetPost)
async def create_post(post: schemas.CreatePost, user: User = Depends(get_user)):
    return await service.post_s.create(post, author_id=user.id)


@post_router.put("/{pk}", responses={404: {"model": HTTPNotFoundError}})
async def update_post(pk: int, post: schemas.UpdatePost, user: User = Depends(get_user)):
    return await service.post_s.update(post, author_id=user.id, id=pk)


@post_router.delete("/{pk}", responses={404: {"model": HTTPNotFoundError}})
async def delete_item(pk: int, user: User = Depends(get_user)):
    return await service.post_s.delete(author_id=user.id, id=pk)
