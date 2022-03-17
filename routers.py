from fastapi import APIRouter

from blog.endpoint import post, comment, tag
from user import api

blog_router = APIRouter()


blog_router.include_router(api.user_router, tags=["user"])
blog_router.include_router(post.post_router, prefix="/post", tags=["post"])
blog_router.include_router(comment.comment_router, prefix="/comment", tags=["comment"])
blog_router.include_router(tag.tag_router, prefix="/tag", tags=["tag"])
