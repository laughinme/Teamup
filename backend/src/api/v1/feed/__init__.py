from fastapi import APIRouter


def get_feed_router() -> APIRouter:
    from .for_you import router as for_you_router
    
    router = APIRouter(prefix='/feed', tags=['Feed'])
    
    router.include_router(for_you_router)
    
    return router
