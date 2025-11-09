from fastapi import APIRouter, Depends

from core.security import require

def get_teams_router() -> APIRouter:
    from .create import router as create_router
    from .catalog import router as catalog_router
    from .team_id import get_team_id_router
    
    router = APIRouter(
        prefix='/teams',
        tags=['Teams'],
        dependencies=[Depends(require("member"))],
        responses={
            401: {"description": "Not authorized"},
            # 409: {"description": "User can be a member of only one team"},
        }
    )
    
    router.include_router(create_router)
    router.include_router(catalog_router)
    router.include_router(get_team_id_router())
    
    return router
