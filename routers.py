from fastapi import APIRouter

from blog.endpoint import post, comment
from user import api

blog_router = APIRouter()


blog_router.include_router(api.user_router, tags=["user"])
blog_router.include_router(post.post_router, prefix="/post", tags=["post"])
blog_router.include_router(comment.comment_router, prefix="/comment", tags=["comment"])
