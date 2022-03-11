from fastapi import Depends, HTTPException, APIRouter

from tortoise.contrib.fastapi import HTTPNotFoundError

from user.settings import current_active_user
from user.models import UserDB
from blog import schemas, models
from blog import service


post_router = APIRouter()


@post_router.get('/post/{pk}', response_model=schemas.GetPost, responses={404: {"model": HTTPNotFoundError}})
async def get_post(pk: int):
    return await service.post_s.get(id=pk)
    # return await schemas.GetPost.from_queryset_single(models.Post.get(id=post_id))


@post_router.post('/post', response_model=schemas.GetPost)
async def create_post(post: schemas.CreatePost, user: UserDB = Depends(current_active_user)):
    post_obj = await models.Post.create(author_id=user.id, **post.dict(exclude_unset=True))
    return await schemas.GetPost.from_tortoise_orm(post_obj)


@post_router.put('/post/{pk}', response_model=schemas.GetPost, responses={404: {"model": HTTPNotFoundError}})
async def update_post(pk: int, post: schemas.UpdatePost, user: UserDB = Depends(current_active_user)):
    await models.Post.filter(id=pk, author_id=user.id).update(**post.dict(exclude_unset=True))
    return await schemas.GetPost.from_queryset_single(models.Post.get(id=pk, author_id=user.id))


@post_router.delete("/post/{pk}", response_model=schemas.Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_post(pk: int, user: UserDB = Depends(current_active_user)):
    deleted_count = await models.Post.filter(id=pk, author_id=user.id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {pk} not found")
    return schemas.Status(message=f"Deleted user {pk}")
