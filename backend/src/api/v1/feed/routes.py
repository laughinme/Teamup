from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from core.security import auth_user
from database.relational_db import User
from domain.feed import FeedItem, FeedResponse
from service.matching import FeedService, get_feed_service


router = APIRouter(prefix="/feed", tags=["feed"])


@router.get(
    "/for-you",
    response_model=FeedResponse,
    summary="Персональные рекомендации",
)
async def feed_for_you(
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[FeedService, Depends(get_feed_service)],
):
    items = await service.get_for_user(user.id)
    return FeedResponse(items=items)


