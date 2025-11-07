from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..interfaces import BaseInterface
from .profiles_table import Profile
from .tech_tags_table import ProfileTechTag, TechTag


class ProfilesInterface(BaseInterface[Profile, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(Profile, session)

    def base_query(self) -> Select[tuple[Profile]]:
        return select(Profile)


class TechTagsInterface(BaseInterface[TechTag, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(TechTag, session)


class ProfileTechTagsInterface(BaseInterface[ProfileTechTag, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(ProfileTechTag, session)


