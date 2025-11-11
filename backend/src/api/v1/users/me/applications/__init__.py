from fastapi import APIRouter


def get_applications_router() -> APIRouter:
    from .routes import router as routes_router
    
    router = APIRouter(prefix='/applications', tags=['Applications'])
    
    router.include_router(routes_router)
    
    return router
