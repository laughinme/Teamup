from fastapi import APIRouter, Depends

from core.security import require

def get_team_id_router() -> APIRouter:
    from .routes import router as routes_router
    from .applications import get_applications_router
    from .invites import get_invites_router
    
    router = APIRouter(prefix='/{team_id}')
    
    router.include_router(routes_router)
    router.include_router(get_applications_router())
    router.include_router(get_invites_router())
    
    return router
