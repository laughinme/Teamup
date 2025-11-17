from typing import Annotated

from fastapi import APIRouter, Depends, Query

from core.security import auth_user, require
from database.relational_db import User
from domain.feed import FeedItem
from domain.common import CursorPage
from domain.errors import NotImplementedHTTPError
# from service.matching import FeedService, get_feed_service


router = APIRouter()


@router.get(
    "/for-you",
    response_model=CursorPage[FeedItem],
    summary="Personal recommendations. (not implemented yet)",
)
async def feed_for_you(
    user: Annotated[User, Depends(auth_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    cursor: Annotated[str | None, Query(description='Opaque cursor')] = None,
    # service: Annotated[FeedService, Depends(get_feed_service)],
):
    # items = await svc.get_for_user(user.id, limit=limit, cursor=cursor)
    # return CursorPage[FeedItem](items=items, next_cursor=None)
    raise NotImplementedHTTPError()
