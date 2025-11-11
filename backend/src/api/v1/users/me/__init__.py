from fastapi import APIRouter


def get_me_router() -> APIRouter:
    from .profile import router as profile_router
    from .picture import router as picture_router
    from .applications import get_applications_router
    from .invites import get_invites_router
    
    # Common router for all child paths
    common_router = APIRouter(prefix='/me')
    
    # Router for user-specific paths
    # This division is mainly made for the purpose of grouping related routes together with tags.
    # This is useful for the purpose of documentation and API reference generation.
    user_specific_router = APIRouter(tags=['Users'])
    
    user_specific_router.include_router(profile_router)
    user_specific_router.include_router(picture_router)
    
    # Router for resource-specific paths
    resource_router = APIRouter()
    resource_router.include_router(get_applications_router())
    resource_router.include_router(get_invites_router())
    
    common_router.include_router(user_specific_router)
    common_router.include_router(resource_router)
    
    return common_router
