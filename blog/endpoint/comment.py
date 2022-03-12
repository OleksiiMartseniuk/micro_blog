from fastapi import Depends, APIRouter

from blog import schemas, service


comment_router = APIRouter()


@comment_router.post('/', response_model=schemas.GetComment)
async def create_comment(comment: schemas.CreateComment):
    # Validate email
    return await service.comment_s.create(comment)
