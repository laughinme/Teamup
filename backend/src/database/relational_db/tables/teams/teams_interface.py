from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .teams_table import Team
from ..interfaces import BaseInterface


class TeamsInterface(BaseInterface[Team, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(Team, session)
