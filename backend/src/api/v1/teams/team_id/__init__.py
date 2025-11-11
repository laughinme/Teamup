from fastapi import APIRouter, Depends

from core.security import require

def get_team_id_router() -> APIRouter:
    from .routes import router as routes_router
    from .applications import get_applications_router
    from .invites import get_invites_router
    
    # Common router for all child paths
    common_router = APIRouter(prefix='/{team_id}')
    
    # Router for team-specific paths
    # This division is mainly made for the purpose of grouping related routes together with tags.
    # This is useful for the purpose of documentation and API reference generation.
    team_router = APIRouter(tags=['Teams'])
    team_router.include_router(routes_router)
    
    # Router for resource-specific paths
    resource_router = APIRouter()
    resource_router.include_router(get_applications_router())
    resource_router.include_router(get_invites_router())
    
    common_router.include_router(team_router)
    common_router.include_router(resource_router)
    
    return common_router
