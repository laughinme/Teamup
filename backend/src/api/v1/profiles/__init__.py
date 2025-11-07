from fastapi import APIRouter

from .routes import router as profiles_router


def get_profiles_router() -> APIRouter:
    return profiles_router


