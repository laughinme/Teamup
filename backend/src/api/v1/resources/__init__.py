from fastapi import APIRouter


def get_resources_router() -> APIRouter:
    from .tech_tags import router as tech_tags_router
    
    router = APIRouter(tags=["Resources"])
    
    router.include_router(tech_tags_router)

    return router
