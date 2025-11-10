from fastapi import APIRouter, Depends

from core.security import require

def get_applications_router() -> APIRouter:
    from .applications import router as applications_router
    from .application_id import get_application_id_router
    
    router = APIRouter(prefix='/applications')
    
    router.include_router(applications_router)
    router.include_router(get_application_id_router())
    
    return router
