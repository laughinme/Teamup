from fastapi import APIRouter, Depends

from core.security import require

def get_application_id_router() -> APIRouter:
    from .routes import router as routes_router
    
    router = APIRouter(prefix='/{application_id}')
    
    router.include_router(routes_router)
    
    return router
