from fastapi import Depends

from database.relational_db import (
    ProfilesInterface,
    ProfileTechTagsInterface,
    TechTagsInterface,
    UoW,
    get_uow,
)

from .profile_service import ProfileService


async def get_profile_service(
    uow: UoW = Depends(get_uow),
) -> ProfileService:
    profiles = ProfilesInterface(uow.session)
    tech_links = ProfileTechTagsInterface(uow.session)
    tech_tags = TechTagsInterface(uow.session)
    return ProfileService(uow, profiles, tech_links, tech_tags)


