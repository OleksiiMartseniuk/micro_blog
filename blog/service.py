from service_base import BaseService
from blog import models, schemas


class PostService(BaseService):
    model = models.Post
    create_schema = schemas.CreatePost
    update_schema = schemas.UpdatePost
    get_schema = schemas.GetPost


class CommentService(BaseService):
    model = models.Comment
    create_schema = schemas.CreatePost
    update_schema = schemas.GetComment
    get_schema = schemas.GetComment


post_s = PostService()
comment_s = CommentService()
