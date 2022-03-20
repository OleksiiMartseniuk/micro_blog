from tortoise import fields, models


class User(models.Model):
    """Model User"""
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=50, unique=True)
    avatar = fields.CharField(max_length=1000)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    def __str__(self):
        return self.username
