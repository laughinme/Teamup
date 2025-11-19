from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..interfaces import BaseInterface
from .profiles_table import Profile
from .profile_tech_tags import ProfileTechTag
from domain.common import Direction, ExperienceLevel, ProfileVisibility


class ProfilesInterface(BaseInterface[Profile, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(Profile, session)

    def base_query(self) -> Select[tuple[Profile]]:
        return select(Profile)
    
    async def initialize_default_profile(self, user_id: UUID) -> Profile:
        profile = Profile(
            id=user_id,
            direction=Direction.FRONTEND,
            # experience_level=ExperienceLevel.MIDDLE,
            # timezone="UTC",
            visibility=ProfileVisibility.PUBLIC,
        )
        await self.add(profile)
        return profile
    

class ProfileTechTagsInterface(BaseInterface[ProfileTechTag, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(ProfileTechTag, session)
