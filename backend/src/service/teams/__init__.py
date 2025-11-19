from fastapi import Depends

from database.relational_db import (
    # TeamApplicationsInterface,
    # TeamInvitesInterface,
    TeamMembershipsInterface,
    TeamNeedsInterface,
    TeamsInterface,
    TechTagsInterface,
    UoW,
    get_uow,
)

from .team_service import TeamService


async def get_team_service(
    uow: UoW = Depends(get_uow),
) -> TeamService:
    teams = TeamsInterface(uow.session)
    needs = TeamNeedsInterface(uow.session)
    memberships = TeamMembershipsInterface(uow.session)
    tech_tags = TechTagsInterface(uow.session)
    # applications = TeamApplicationsInterface(uow.session)
    # invites = TeamInvitesInterface(uow.session)
    return TeamService(uow, teams, needs, memberships, tech_tags)
