from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .teams_table import Team


class TeamsInterface:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def add(self, team: Team) -> Team:
        self.session.add(team)
        return team
    
    async def get_by_id(self, id: UUID | str) -> Team | None:
        stmt = select(Team).where(Team.id == id)
        return await self.session.scalar(stmt)
