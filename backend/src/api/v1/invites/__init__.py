from fastapi import APIRouter

from .routes import router as invites_router


def get_invites_router() -> APIRouter:
    return invites_router


