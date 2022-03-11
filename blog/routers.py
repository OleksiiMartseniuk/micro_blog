
from fastapi import APIRouter
from blog.endpoint import post


blog_router = APIRouter()


blog_router.include_router(post.post_router, prefix="/post", tags=["blog"])
