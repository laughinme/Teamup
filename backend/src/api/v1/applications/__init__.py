from fastapi import APIRouter

from .routes import router as applications_router


def get_applications_router() -> APIRouter:
    return applications_router


