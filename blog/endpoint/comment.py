from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from blog import schemas, service


comment_router = APIRouter()


@comment_router.post('', response_model=schemas.GetComment)
async def create_comment(comment: schemas.CreateComment):
    return await service.comment_s.create(comment)


@comment_router.delete('/{pk}', response_model=schemas.Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_comment(pk: int):
    return await service.comment_s.delete(id=pk)
