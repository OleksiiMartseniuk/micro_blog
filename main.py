from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from routers import blog_router


app = FastAPI()


app.include_router(blog_router)

register_tortoise(
    app,
    db_url="sqlite://blog.db",
    modules={"models": ["blog.models", "user.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
