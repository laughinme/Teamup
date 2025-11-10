from fastapi import APIRouter


def get_me_router() -> APIRouter:
    from .profile import router as profile_router
    from .picture import router as picture_router
    from .applications import get_applications_router
    from .invites import get_invites_router
    
    router = APIRouter(prefix='/me')
    
    router.include_router(profile_router)
    router.include_router(picture_router)
    router.include_router(get_applications_router())
    router.include_router(get_invites_router())
    
    return router
