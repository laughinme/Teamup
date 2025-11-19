from fastapi import APIRouter


def get_v1_router() -> APIRouter:
    from .auth import get_auth_routers
    from .users import get_users_router
    from .profiles import get_profiles_router
    from .teams import get_teams_router
    from .feed import get_feed_router
    from .resources import get_resources_router
    from .misc import get_misc_router
    from .admin import get_admin_router
    
    router = APIRouter(prefix='/v1')

    router.include_router(get_auth_routers())
    router.include_router(get_users_router())
    router.include_router(get_profiles_router())
    router.include_router(get_teams_router())
    router.include_router(get_feed_router())
    router.include_router(get_resources_router())
    router.include_router(get_misc_router())
    router.include_router(get_admin_router())
    
    return router
