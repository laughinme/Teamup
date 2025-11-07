from fastapi import Depends

from database.redis import CacheRepo, get_redis

from .feed_service import FeedService


async def get_feed_service(redis=Depends(get_redis)) -> FeedService:
    cache = CacheRepo(redis) if redis else None
    return FeedService(cache)


