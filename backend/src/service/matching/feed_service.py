from __future__ import annotations

from uuid import UUID

from database.redis import CacheRepo
from domain.feed import FeedItem, FeedEntityType


class FeedService:
    def __init__(self, cache: CacheRepo | None = None) -> None:
        self.cache = cache

    async def get_for_user(self, user_id: UUID) -> list[FeedItem]:
        # TODO: implement scoring logic and Redis caching (PRD section 13)
        _ = user_id
        return []


