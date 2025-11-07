from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .teams_table import Team
from .team_memberships import TeamMembership
from .team_applications import TeamApplication
from .team_invites import TeamInvite
from .team_needs import TeamNeed
from ..interfaces import BaseInterface


class TeamsInterface(BaseInterface[Team, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(Team, session)


class TeamMembershipsInterface(BaseInterface[TeamMembership, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(TeamMembership, session)


class TeamApplicationsInterface(BaseInterface[TeamApplication, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(TeamApplication, session)


class TeamInvitesInterface(BaseInterface[TeamInvite, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(TeamInvite, session)


class TeamNeedsInterface(BaseInterface[TeamNeed, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(TeamNeed, session)
