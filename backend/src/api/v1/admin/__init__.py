from fastapi import APIRouter


def get_admin_router() -> APIRouter:
    from .routes import router as routes_router
    
    router = APIRouter(prefix='/admin', tags=['Admin'], include_in_schema=False)
    
    router.include_router(routes_router)
    
    return router
