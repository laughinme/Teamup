from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .teams_table import Team
from .team_memberships import TeamMembership
from .team_needs import TeamNeed
from .tech_tags_table import TechTag
from ..interfaces import BaseInterface


class TeamsInterface(BaseInterface[Team, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(Team, session)
        
    async def list_teams(self, *, limit: int = 50, offset: int = 0) -> list[Team]:
        stmt = select(Team).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return list(result.all())

class TeamMembershipsInterface():
    def __init__(self, session: AsyncSession):
        self.session = session

class TeamNeedsInterface(BaseInterface[TeamNeed, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(TeamNeed, session)


class TechTagsInterface(BaseInterface[TechTag, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(TechTag, session)
