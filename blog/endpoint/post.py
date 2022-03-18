from typing import Optional, List

from fastapi import (Depends,
                     APIRouter,
                     UploadFile,
                     File,
                     Form,
                     BackgroundTasks,
                     HTTPException)

from user.auth import get_user
from user.models import User
from blog import schemas, service
from tortoise.contrib.fastapi import HTTPNotFoundError


post_router = APIRouter()


@post_router.get('/{pk}', response_model=schemas.GetPost, responses={404: {"model": HTTPNotFoundError}})
async def get_post(pk: int):
    return await service.post_s.get(id=pk)


@post_router.get('', response_model=List[schemas.GetPost])
async def list_post():
    return await service.post_s.list()


@post_router.post('', response_model=schemas.GetPost, responses={404: {"model": HTTPNotFoundError}})
async def create_post(
        background_tasks: BackgroundTasks,
        title: str = Form(...),
        body: str = Form(...),
        file: Optional[UploadFile] = File(None),
        tag: Optional[List[int]] = Form(None),
        user: User = Depends(get_user)
        ):
    if not file:
        obj = await service.post_s.create(title=title,
                                          body=body,
                                          author_id=user.id)
    else:
        file_name = f'media/{file.filename}'
        if file.content_type == 'image/jpeg':
            background_tasks.add_task(service.write_image, file_name, file)
            obj = await service.post_s.create(title=title,
                                              body=body,
                                              image=file_name,
                                              author_id=user.id)
        else:
            raise HTTPException(status_code=418, detail="It isn't image")
    if tag:
        tag_db = await service.get_tag(tag)
        await obj.tag.add(*tag_db)
    return await schemas.GetPost.from_tortoise_orm(obj)


# add  update
@post_router.put("/{pk}", responses={404: {"model": HTTPNotFoundError}})
async def update_post(pk: int, post: schemas.UpdatePost, user: User = Depends(get_user)):
    return await service.post_s.update(post, author_id=user.id, id=pk)


@post_router.delete("/{pk}", responses={404: {"model": HTTPNotFoundError}})
async def delete_item(pk: int, user: User = Depends(get_user)):
    return await service.post_s.delete(author_id=user.id, id=pk)
