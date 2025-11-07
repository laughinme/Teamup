from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import delete, select

from database.relational_db import (
    Team,
    TeamApplicationsInterface,
    TeamInvitesInterface,
    TeamMembershipsInterface,
    TeamNeed,
    TeamNeedsInterface,
    TeamsInterface,
    UoW,
)
from domain.teams import TeamCreate, TeamNeedInput, TeamUpdate, TeamStatus


class TeamService:
    def __init__(
        self,
        uow: UoW,
        teams: TeamsInterface,
        needs: TeamNeedsInterface,
        memberships: TeamMembershipsInterface,
        applications: TeamApplicationsInterface,
        invites: TeamInvitesInterface,
    ) -> None:
        self.uow = uow
        self.teams = teams
        self.needs = needs
        self.memberships = memberships
        self.applications = applications
        self.invites = invites

    async def get_team(self, team_id: UUID) -> Team | None:
        return await self.teams.get_by_id(team_id)

    async def list_teams(self, *, limit: int = 50, offset: int = 0) -> list[Team]:
        stmt = select(Team).limit(limit).offset(offset)
        result = await self.uow.session.scalars(stmt)
        return result.unique().all()

    async def create_team(self, *, owner_id: UUID, payload: TeamCreate) -> Team:
        team = Team(
            id=uuid4(),
            created_by_user_id=owner_id,
            name=payload.name,
            description=payload.description,
            direction=payload.direction,
            visibility=payload.visibility,
            max_members=payload.max_members,
            status=TeamStatus.DRAFT,
        )
        team = await self.teams.add(team)
        await self._sync_needs(team, payload.needs)
        await self.uow.commit()
        await self.uow.session.refresh(team)
        return team

    async def update_team(self, *, team: Team, payload: TeamUpdate) -> Team:
        data = payload.model_dump(exclude_unset=True, exclude={"needs"})
        for field, value in data.items():
            setattr(team, field, value)

        if payload.needs is not None:
            await self._sync_needs(team, payload.needs)

        await self.uow.commit()
        await self.uow.session.refresh(team)
        return team

    async def _sync_needs(self, team: Team, inputs: list[TeamNeedInput]) -> None:
        await self.uow.session.execute(
            delete(TeamNeed).where(TeamNeed.team_id == team.id)
        )
        if not inputs:
            await self.uow.session.flush()
            return

        needs: list[TeamNeed] = []
        for entry in inputs:
            needs.append(
                TeamNeed(
                    id=entry.id or uuid4(),
                    team_id=team.id,
                    direction=entry.direction,
                    required_level=entry.required_level,
                    must_tag_ids=entry.must_tag_ids,
                    nice_tag_ids=entry.nice_tag_ids,
                    slots=entry.slots,
                    notes=entry.notes,
                )
            )
        self.uow.session.add_all(needs)
        await self.uow.session.flush()


