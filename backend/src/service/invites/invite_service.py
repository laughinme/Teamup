from __future__ import annotations

from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlalchemy import select

from database.relational_db import TeamInvite, TeamInvitesInterface, UoW
from domain.invites import InviteCreate
from domain.teams import TeamInviteStatus


class InviteService:
    def __init__(self, uow: UoW, invites: TeamInvitesInterface) -> None:
        self.uow = uow
        self.invites = invites

    async def get_invite(self, invite_id: UUID) -> TeamInvite | None:
        return await self.invites.get_by_id(invite_id)

    async def create_invite(
        self,
        *,
        team_id: UUID,
        invited_user_id: UUID,
        invited_by_user_id: UUID,
        payload: InviteCreate,
    ) -> TeamInvite:
        invite = TeamInvite(
            id=uuid4(),
            team_id=team_id,
            invited_user_id=invited_user_id,
            invited_by_user_id=invited_by_user_id,
            message=payload.message,
            expires_at=payload.expires_at,
            status=TeamInviteStatus.PENDING,
        )
        invite = await self.invites.add(invite)
        await self.uow.commit()
        await self.uow.session.refresh(invite)
        return invite

    async def list_for_user(
        self,
        *,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> list[TeamInvite]:
        stmt = (
            select(TeamInvite)
            .where(TeamInvite.invited_user_id == user_id)
            .limit(limit)
            .offset(offset)
            .order_by(TeamInvite.created_at.desc())
        )
        result = await self.uow.session.scalars(stmt)
        return result.unique().all()

    async def update_status(
        self,
        invite: TeamInvite,
        status: TeamInviteStatus,
    ) -> TeamInvite:
        invite.status = status
        invite.responded_at = datetime.now(UTC)
        await self.uow.commit()
        await self.uow.session.refresh(invite)
        return invite


