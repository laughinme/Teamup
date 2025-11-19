from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import delete, select

from database.relational_db import (
    Team,
    # TeamApplicationsInterface,
    # TeamInvitesInterface,
    TeamMembershipsInterface,
    TeamNeed,
    TeamNeedsInterface,
    TeamsInterface,
    UoW,
    TeamNeedTag,
    TechTag,
    TechTagsInterface,
)
from domain.teams import (
    NeedRequirementType,
    TeamCreate,
    TeamNeedInput,
    TeamUpdate,
    TeamStatus,
)
from domain.errors import BadRequestHTTPError


class TeamService:
    def __init__(
        self,
        uow: UoW,
        teams: TeamsInterface,
        needs: TeamNeedsInterface,
        memberships: TeamMembershipsInterface,
        tech_tags: TechTagsInterface,
        # applications: TeamApplicationsInterface,
        # invites: TeamInvitesInterface,
    ) -> None:
        self.uow = uow
        self.session = uow.session
        self.teams = teams
        self.needs = needs
        self.memberships = memberships
        self.tech_tags = tech_tags
        # self.applications = applications
        # self.invites = invites

    async def get_team(self, team_id: UUID) -> Team | None:
        return await self.teams.get_by_id(team_id)

    async def list_teams(self, *, limit: int = 50, offset: int = 0) -> list[Team]:
        stmt = select(Team).limit(limit).offset(offset)
        result = await self.uow.session.scalars(stmt)
        return list(result.unique().all())

    async def create_team(self, *, owner_id: UUID, payload: TeamCreate) -> Team:
        team = Team(
            id=uuid4(),
            created_by_user_id=owner_id,
            name=payload.name,
            description=payload.description,
            # direction=payload.direction,
            max_members=payload.max_members,
            current_members=1,
            status=TeamStatus.DRAFT,
            visibility=payload.visibility,
        )
        team = await self.teams.add(team)
        await self._sync_needs(team, payload.needs)
        await self.uow.commit()
        await self.session.refresh(team)
        return team

    async def update_team(self, *, team: Team, payload: TeamUpdate) -> Team:
        data = payload.model_dump(exclude_unset=True, exclude={"needs"})
        for field, value in data.items():
            setattr(team, field, value)

        if payload.needs is not None:
            await self._sync_needs(team, payload.needs)

        await self.uow.commit()
        await self.session.refresh(team)
        return team

    async def _sync_needs(self, team: Team, inputs: list[TeamNeedInput]) -> None:
        await self.uow.session.execute(
            delete(TeamNeed).where(TeamNeed.team_id == team.id)
        )
        
        await self.session.refresh(team, ["needs"])
        
        for entry in inputs:
            need = TeamNeed(
                team_id=team.id,
                direction=entry.direction,
                required_level=entry.required_level,
                slots=entry.slots,
                notes=entry.notes,
            )

            team.needs.append(need)
            
            need.must_tags = [
                TeamNeedTag(
                    tag_id=tag_id,
                    requirement_type=NeedRequirementType.MUST,
                )
                for tag_id in entry.must_tag_ids
            ]
            need.nice_tags = [
                TeamNeedTag(
                    tag_id=tag_id,
                    requirement_type=NeedRequirementType.NICE,
                )
                for tag_id in entry.nice_tag_ids
            ]
            
            
        # await self.uow.session.flush()


    async def list_tech_tags(
        self,
        *,
        query: str = "",
        limit: int = 20,
        cursor: str | None = None,
    ) -> tuple[list[TechTag], str | None]:
        cursor_created_at = None
        cursor_id = None
        if cursor:
            try:
                ts_str, id_str = cursor.split("_", 1)
                cursor_created_at = datetime.fromisoformat(ts_str)
                cursor_id = UUID(id_str)
            except Exception:
                raise BadRequestHTTPError(detail='Invalid cursor')

        tech_tags = await self.tech_tags.list_tech_tags(
            query=query,
            limit=limit,
            cursor_created_at=cursor_created_at,
            cursor_id=cursor_id,
        )

        next_cursor = None
        if len(tech_tags) == limit:
            last = tech_tags[-1]
            if last.created_at is None:
                next_cursor = None
            else:
                next_cursor = f"{last.created_at.isoformat()}_{last.id}"

        return tech_tags, next_cursor
