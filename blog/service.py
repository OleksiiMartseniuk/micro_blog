import shutil
from fastapi import UploadFile

from service_base import BaseService
from blog import models, schemas


class PostService(BaseService):
    model = models.Post
    create_schema = schemas.CreatePost
    update_schema = schemas.GetPost
    get_schema = schemas.GetPost

    async def create(self, **kwargs):
        obj = await self.model.create(**kwargs)
        return await self.get_schema.from_tortoise_orm(obj)


class CommentService(BaseService):
    model = models.Comment
    create_schema = schemas.CreatePost
    update_schema = schemas.GetComment
    get_schema = schemas.GetComment


post_s = PostService()
comment_s = CommentService()


def write_image(file_name: str, file: UploadFile):
    # write image
    with open(file_name, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
