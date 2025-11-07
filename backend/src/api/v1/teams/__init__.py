from fastapi import APIRouter

from .routes import router as teams_router


def get_teams_router() -> APIRouter:
    return teams_router

from fastapi import APIRouter, Depends

from core.security import require


def get_teams_router() -> APIRouter:
    from .create import router as create_team_router
    
    router = APIRouter(
        prefix='/teams',
        tags=['Teams'],
        dependencies=[Depends(require("member"))],
        responses={
            401: {"description": "Not authorized"},
            # 409: {"description": "User can be a member of only one team"},
        }
    )
    
    router.include_router(create_team_router)
    
    return router
