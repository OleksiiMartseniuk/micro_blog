import ormar
from db import BaseMeta


class User(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100, unique=True)
    phone: str = ormar.String(max_length=14, unique=True, nullable=True)
    email: str = ormar.String(index=True, unique=True, nullable=False, max_length=255)
    avatar: str = ormar.String(max_length=500, nullable=True)
    is_active: bool = ormar.Boolean(default=True, nullable=False)
    is_superuser: bool = ormar.Boolean(default=False, nullable=False)
