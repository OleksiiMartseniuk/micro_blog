from service_base import BaseService
from blog import models, schemas


class PostService(BaseService):
    model = models.Post
    create_schema = schemas.CreatePost
    update_schema = schemas.UpdatePost
    get_schema = schemas.GetPost


post_s = PostService()
