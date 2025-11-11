from fastapi import APIRouter


def get_invites_router() -> APIRouter:
    from .routes import router as routes_router
    
    router = APIRouter(prefix='/invites', tags=['Invites'])
    
    router.include_router(routes_router)
    
    return router
