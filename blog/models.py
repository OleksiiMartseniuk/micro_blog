from tortoise import fields, models


class Post(models.Model):
    """Model Post"""
    title = fields.CharField(max_length=200)
    author = fields.ForeignKeyField('models.User', related_name='post')
    body = fields.TextField()
    image = fields.CharField(max_length=500, null=True)
    publish = fields.DatetimeField(auto_now_add=True)
    # draft | published
    status = fields.CharField(max_length=9, default='published')
    tag: fields.ManyToManyRelation['Tag'] = fields.ManyToManyField(
        'models.Tag', related_name='posts', through='post_tag'
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Model Comment"""
    post = fields.ForeignKeyField('models.Post', related_name='comment_post')
    name = fields.CharField(max_length=200)
    email = fields.CharField(max_length=50)
    body = fields.CharField(max_length=255)
    create = fields.DatetimeField(auto_now_add=True)
    active = fields.BooleanField(default=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Model Tag"""
    name = fields.CharField(max_length=30, unique=True)
    posts: fields.ManyToManyRelation[Post]

    def __str__(self):
        return self.name
