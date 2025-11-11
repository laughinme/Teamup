from fastapi import APIRouter


def get_profiles_router() -> APIRouter:
    from .routes import router as profiles_router
    
    router = APIRouter(prefix="/profiles", tags=["Profiles"])
    
    router.include_router(profiles_router)

    return router
