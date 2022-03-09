import ormar
from datetime import datetime

from typing import Optional
from db import BaseMeta
from user.models import User
from tag.models import Tag
from enum import Enum


class StatusChoices(Enum):
    draft = 'Draft'
    published = 'Published'


class Post(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=200)
    author: Optional[User] = ormar.ForeignKey(User, related_name='user_post')
    body: str = ormar.String(max_length=1000)
    publish: datetime = ormar.DateTime(default=datetime.now)
    status: str = ormar.String(max_length=9, default=StatusChoices.draft.value, choices=list(StatusChoices))
    tags: Optional[Tag] = ormar.ManyToMany(Tag)



