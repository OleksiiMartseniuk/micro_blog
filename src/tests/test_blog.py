import pytest
from httpx import AsyncClient
from main import app

from src.user.models import User


@pytest.mark.asyncio
async def test_user():
    assert await User.all().count() == 0
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/google/auth")
    print(response.json())
    # assert await User.all().count() == 1
