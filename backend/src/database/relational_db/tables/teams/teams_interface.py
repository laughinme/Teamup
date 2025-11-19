from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, or_, and_
from datetime import datetime

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
    
    
    async def list_tech_tags(
        self, 
        *,
        query: str = "",
        limit: int = 20,
        cursor_created_at: datetime | None = None,
        cursor_id: UUID | None = None,
    ) -> list[TechTag]:
        stmt = select(TechTag)
        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(or_(TechTag.name.ilike(pattern), TechTag.slug.ilike(pattern)))
        
        if cursor_created_at is not None and cursor_id is not None:
            stmt = stmt.where(
                or_(
                    TechTag.created_at < cursor_created_at,
                    and_(TechTag.created_at == cursor_created_at, TechTag.id < cursor_id),
                )
            )
            
        stmt = stmt.order_by(TechTag.created_at.desc(), TechTag.id.desc()).limit(limit)
        
        result = await self.session.scalars(stmt)
        return list(result.all())
