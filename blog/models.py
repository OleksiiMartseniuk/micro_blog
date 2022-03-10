from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Tag(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)


class Post(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    author = fields.ForeignKeyField('models.UserModel', related_name='posts')
    body = fields.TextField()
    publish = fields.DatetimeField(auto_now_add=True)
    # draft | published
    status = fields.CharField(max_length=9)
    tags = fields.ManyToManyField('models.Tag')


class Comment(models.Model):
    id = fields.IntField(pk=True)
    post = fields.ForeignKeyField('models.Post', related_name='comments')
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=10)
    body = fields.CharField(max_length=250)
    create = fields.DatetimeField(auto_now_add=True)
    active = fields.BooleanField(default=True)


Tag_Pydantic = pydantic_model_creator(Tag, name="Tag")
Post_Pydantic = pydantic_model_creator(Post, name="Post")
Comment_Pydantic = pydantic_model_creator(Comment, name="Comment")
