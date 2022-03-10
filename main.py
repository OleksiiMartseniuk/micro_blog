from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from blog.api import blog_router
from user.api import user_router

from user.settings import auth_backend, fastapi_users


app = FastAPI()

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

app.include_router(user_router)
app.include_router(blog_router)

register_tortoise(
    app,
    db_url="sqlite://blog.db",
    modules={"models": ["blog.models", "user.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
