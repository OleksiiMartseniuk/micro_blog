import pytest
from httpx import AsyncClient
from main import app

from src.user.models import User
from src.user import tokenizator
from src.blog.models import Post, Comment


async def get_user_token() -> str:
    """Token user"""
    user = await User.first()
    internal_token = tokenizator.create_token(user.id)
    return internal_token.get("access_token")


@pytest.mark.asyncio
async def test_user_me():
    user_token = await get_user_token()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user/me", headers={"Authorization": f"Bearer {user_token}"})
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'user@example.com',
        'avatar': 'path/test',
        'is_active': True,
        'is_superuser': False
    }


@pytest.mark.asyncio
async def test_post_create_default():
    user_token = await get_user_token()
    assert await Post.all().count() == 0
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/post",
                                 data={"title": "name", "body": "disc"},
                                 headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert await Post.all().count() == 1
    assert response.json() == {
        'id': 1,
        'title': 'name',
        'body': 'disc',
        'image': None,
        'publish': response.json()['publish'],
        'status': 'published'
    }


@pytest.mark.asyncio
async def test_comment_create():
    assert await Comment.all().count() == 0
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/comment", json={
            "post_id": 1,
            "name": "string",
            "email": "user@example.com",
            "body": "string"
        })
    assert response.status_code == 200
    assert await Comment.all().count() == 1
    assert response.json() == {
        'id': 1,
        'name': 'string',
        'email': 'user@example.com',
        'body': 'string',
        'create': response.json()['create'],
        'active': True
    }


@pytest.mark.asyncio
async def test_comment_delete():
    assert await Comment.all().count() == 1
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/comment/1?email=user@example.com")
    assert response.status_code == 200
    assert await Comment.all().count() == 0
