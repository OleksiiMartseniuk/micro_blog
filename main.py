from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.routers import blog_router
from src.config import settings

app = FastAPI()

app.include_router(blog_router)

register_tortoise(
    app,
    db_url=settings.DATABASE_URI,
    modules={"models": settings.APPS_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)
