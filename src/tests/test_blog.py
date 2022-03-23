import pytest
from httpx import AsyncClient
from main import app

from src.user.models import User
from src.user import tokenizator
from src.blog.models import Post, Comment, Tag
from src.config.settings import BASE_DIR


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


@pytest.mark.asyncio
async def test_tag_create():
    user_token = await get_user_token()
    assert await Tag.all().count() == 0
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/tag",
                                 json={'name': 'test_tag'},
                                 headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert await Tag.all().count() == 1
    assert response.json() == {'id': 1, 'name': 'test_tag'}


@pytest.mark.asyncio
async def test_tag_get():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/tag/1")
    assert response.json() == {'id': 1, 'name': 'test_tag'}


async def test_tag_list():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/tag")
    assert response.json() == [{'id': 1, 'name': 'test_tag'}]


@pytest.mark.asyncio
async def test_post_create_image_tag():
    filename = f'{BASE_DIR}/src/tests/test_image.jpg'
    user_token = await get_user_token()
    assert await Post.all().count() == 1
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/post",
                                 files={"file": ("test_image", open(filename, "rb"), "image/jpeg")},
                                 data={"title": "name1", "body": "disc1", "tag": 1},
                                 headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert await Post.all().count() == 2
    assert response.json() == {
        'id': 2,
        'title': 'name1',
        'body': 'disc1',
        'image': 'media/test_image',
        'publish': response.json().get('publish'),
        'status': 'published'
    }
    post = await Post.get(id=2)
    assert await post.tag.all().count() == 1


@pytest.mark.asyncio
async def test_post_get():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/post/1')
    assert response.json() == {
        'id': 1,
        'title': 'name',
        'body': 'disc',
        'image': None,
        'publish': response.json().get('publish'),
        'status': 'published'
    }


@pytest.mark.asyncio
async def test_post_list():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/post')
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_post_update():
    user_token = await get_user_token()
    post = await Post.get(id=1)
    assert await post.tag.all().count() == 0
    assert post.title == 'name'
    assert post.body == 'disc'
    assert await post.tag.all().count() == 0
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/post",
                                data={"pk": 1, "title": "name2", "body": "disc2", "tag": 1},
                                headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    post = await Post.get(id=1)
    assert post.title == 'name2'
    assert post.body == 'disc2'
    assert await post.tag.all().count() == 1
    assert response.json() == {'title': 'name2', 'body': 'disc2', 'image': None}


@pytest.mark.asyncio
async def test_post_get_tags():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/post/tags/1")
    assert response.json() == [{'id': 1, 'name': 'test_tag'}]


@pytest.mark.asyncio
async def test_post_delete():
    user_token = await get_user_token()
    assert await Post.get_or_none(id=1)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/post/1", headers={"Authorization": f"Bearer {user_token}"})
    print(response.json())
    assert await Post.get_or_none(id=1) is None
