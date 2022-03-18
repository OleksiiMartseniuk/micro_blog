from fastapi import APIRouter, Depends

from typing import List

from tortoise.contrib.fastapi import HTTPNotFoundError

from blog import schemas, service
from user.models import User
from user.auth import get_user


tag_router = APIRouter()


@tag_router.get('', response_model=List[schemas.GetTag])
async def list_tag():
    return await service.tag_s.list()


@tag_router.get('/{pk}', response_model=schemas.GetTag, responses={404: {"model": HTTPNotFoundError}})
async def get_tag(pk: int):
    return await service.tag_s.get(id=pk)


@tag_router.post('', response_model=schemas.GetTag)
async def crate_tag(tag: schemas.CreateTag, user: User = Depends(get_user)):
    return await service.tag_s.create(tag)


