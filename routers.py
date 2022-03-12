from fastapi import APIRouter

from blog.endpoint import post, comment
from user.settings import auth_backend, fastapi_users


blog_router = APIRouter()


blog_router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
blog_router.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
# app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
# app.include_router(fastapi_users.get_verify_router(), prefix="/auth", tags=["auth"])
blog_router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

blog_router.include_router(post.post_router, prefix="/post", tags=["post"])
blog_router.include_router(comment.comment_router, prefix="/comment", tags=["comment"])
