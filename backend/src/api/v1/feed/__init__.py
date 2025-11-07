from fastapi import APIRouter

from .routes import router as feed_router


def get_feed_router() -> APIRouter:
    return feed_router


