from fastapi import APIRouter

from .routes import router as admin_router


def get_admin_router() -> APIRouter:
    return admin_router


