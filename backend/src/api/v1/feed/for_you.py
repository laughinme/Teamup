from typing import Annotated

from fastapi import APIRouter, Depends

from core.security import auth_user, require
from database.relational_db import User
from domain.feed import FeedItem
from domain.common import CursorPage
from domain.errors import NotImplementedHTTPError
# from service.matching import FeedService, get_feed_service


router = APIRouter(prefix="/feed", tags=["feed"])


@router.get(
    "/for-you",
    response_model=CursorPage[FeedItem],
    summary="Personal recommendations",
)
async def feed_for_you(
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[FeedService, Depends(get_feed_service)],
):
    # items = await service.get_for_user(user.id)
    # return CursorPage[FeedItem](items=items, next_cursor=None)
    raise NotImplementedHTTPError()
