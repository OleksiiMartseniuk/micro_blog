from typing import Optional, List

from fastapi import (Depends,
                     APIRouter,
                     UploadFile,
                     File,
                     Form,
                     BackgroundTasks,
                     HTTPException)

from src.user.auth import get_user
from src.user.models import User
from src.blog import schemas, service
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


@post_router.put('', response_model=schemas.UpdatePost, responses={404: {"model": HTTPNotFoundError}})
async def update_post(
        background_tasks: BackgroundTasks,
        pk: int = Form(...),
        title: Optional[str] = Form(None),
        body: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        tag: Optional[List[int]] = Form(None),
        user: User = Depends(get_user)
):
    if not file:
        post = schemas.UpdatePost(title=title, body=body)
        await service.post_s.update(post, id=pk, author_id=user.id)
    else:
        file_name = f'media/{file.filename}'
        if file.content_type == 'image/jpeg':
            background_tasks.add_task(service.write_image, file_name, file)
            post = schemas.UpdatePost(title=title, body=body, image=file_name)
            await service.post_s.update(post, id=pk, author_id=user.id)
        else:
            raise HTTPException(status_code=418, detail="It isn't image")
    if tag:
        obj = await service.get_post(id=pk, author_id=user.id)
        tag_db = await service.get_tag(tag)
        tag_del = await obj.tag
        await obj.tag.remove(*tag_del)
        await obj.tag.add(*tag_db)
    return post


@post_router.delete('/{pk}', responses={404: {"model": HTTPNotFoundError}})
async def delete_item(pk: int, user: User = Depends(get_user)):
    return await service.post_s.delete(author_id=user.id, id=pk)


@post_router.get('/tags/{pk}', response_model=List[schemas.GetTag], responses={404: {"model": HTTPNotFoundError}})
async def get_tags_post(pk: int):
    return await service.post_s.get_tags_post(id=pk)
