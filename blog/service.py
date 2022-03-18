import shutil
from typing import List
from fastapi import UploadFile

from service_base import BaseService
from blog import models, schemas


class PostService(BaseService):
    model = models.Post
    create_schema = schemas.CreatePost
    update_schema = schemas.GetPost
    get_schema = schemas.GetPost

    async def create(self, **kwargs) -> models.Post:
        obj = await self.model.create(**kwargs)
        return obj


class CommentService(BaseService):
    model = models.Comment
    create_schema = schemas.CreatePost
    get_schema = schemas.GetComment


class TagService(BaseService):
    model = models.Tag
    create_schema = schemas.CreateTag
    get_schema = schemas.GetTag


post_s = PostService()
comment_s = CommentService()
tag_s = TagService()


def write_image(file_name: str, file: UploadFile) -> None:
    # write image
    with open(file_name, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)


async def get_tag(pk_list: list) -> List[models.Tag]:
    return await models.Tag.filter(id__in=pk_list)
