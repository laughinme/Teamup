from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.security import auth_user
from database.relational_db import User
from domain.invites import InviteCreate, InviteListResponse, InviteModel
from domain.teams import TeamInviteStatus
from service.invites import InviteService, get_invite_service
from service.teams import TeamService, get_team_service


router = APIRouter(prefix="", tags=["invites"])


@router.post(
    "/teams/{team_id}/invites",
    response_model=InviteModel,
    status_code=status.HTTP_201_CREATED,
    summary="Отправить инвайт пользователю",
)
async def send_invite(
    team_id: UUID,
    payload: InviteCreate,
    user: Annotated[User, Depends(auth_user)],
    invite_service: Annotated[InviteService, Depends(get_invite_service)],
    team_service: Annotated[TeamService, Depends(get_team_service)],
):
    team = await team_service.get_team(team_id)
    if not team:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    if team.created_by_user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not a team owner")

    invite = await invite_service.create_invite(
        team_id=team_id,
        invited_user_id=payload.user_id,
        invited_by_user_id=user.id,
        payload=payload,
    )
    return InviteModel.model_validate(invite)


@router.get(
    "/me/invites",
    response_model=InviteListResponse,
    summary="Инвайты для пользователя",
)
async def list_my_invites(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    user: Annotated[User, Depends(auth_user)] = Depends(),
    invite_service: Annotated[InviteService, Depends(get_invite_service)] = Depends(),
):
    invites = await invite_service.list_for_user(user_id=user.id, limit=limit, offset=offset)
    items = [InviteModel.model_validate(invite) for invite in invites]
    return InviteListResponse(items=items, next_cursor=None)


async def _change_invite_status(
    invite_id: UUID,
    status_target: TeamInviteStatus,
    invite_service: InviteService,
    user: User,
) -> InviteModel:
    invite = await invite_service.get_invite(invite_id)
    if not invite:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Invite not found")
    if invite.invited_user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not a recipient")
    invite = await invite_service.update_status(invite, status_target)
    return InviteModel.model_validate(invite)


@router.post(
    "/invites/{invite_id}/accept",
    response_model=InviteModel,
    summary="Принять инвайт",
)
async def accept_invite(
    invite_id: UUID,
    user: Annotated[User, Depends(auth_user)],
    invite_service: Annotated[InviteService, Depends(get_invite_service)],
):
    return await _change_invite_status(
        invite_id,
        TeamInviteStatus.ACCEPTED,
        invite_service,
        user,
    )


@router.post(
    "/invites/{invite_id}/reject",
    response_model=InviteModel,
    summary="Отклонить инвайт",
)
async def reject_invite(
    invite_id: UUID,
    user: Annotated[User, Depends(auth_user)],
    invite_service: Annotated[InviteService, Depends(get_invite_service)],
):
    return await _change_invite_status(
        invite_id,
        TeamInviteStatus.REJECTED,
        invite_service,
        user,
    )


