from fastapi import APIRouter, Depends

from core.security import require

def get_applications_router() -> APIRouter:
    from .applications import router as applications_router
    
    router = APIRouter(prefix='/applications')
    
    router.include_router(applications_router)
    
    return router
