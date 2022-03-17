from fastapi import APIRouter, Depends

from blog import schemas, service
from user.models import User
from user.auth import get_user


tag_router = APIRouter()


@tag_router.post('', response_model=schemas.GetTag)
async def crate_tag(tag: schemas.CreateTag, user: User = Depends(get_user)):
    return await service.tag_s.create(tag)

# add list tag
