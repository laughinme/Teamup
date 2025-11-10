from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.security import auth_user
from database.relational_db import User
from domain.invites import InviteCreate, InviteModel
from domain.teams import TeamInviteStatus
from domain.common import CursorPage
from domain.errors import NotImplementedHTTPError
# from service.invites import InviteService, get_invite_service
# from service.teams import TeamService, get_team_service


router = APIRouter()


@router.get(
    "/",
    response_model=CursorPage[InviteModel],
    summary="List invites sent to me",
)
async def list_invites_sent_to_me(
    user: Annotated[User, Depends(auth_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    cursor: Annotated[str | None, Query(description='Opaque cursor')] = None,
    # svc: Annotated[InviteService, Depends(get_invite_service)],
):
    raise NotImplementedHTTPError()


@router.post(
    "/{invite_id}/accept",
    response_model=InviteModel,
    summary="Accept invite",
)
async def accept_invite(
    invite_id: UUID,
    user: Annotated[User, Depends(auth_user)],
    # svc: Annotated[InviteService, Depends(get_invite_service)],
):
    # return await svc.update_status(
    #     invite_id,
    #     TeamInviteStatus.ACCEPTED,
    #     user,
    # )
    raise NotImplementedHTTPError()


@router.post(
    "/{invite_id}/reject",
    response_model=InviteModel,
    summary="Reject invite",
)
async def reject_invite(
    invite_id: UUID,
    user: Annotated[User, Depends(auth_user)],
    # svc: Annotated[InviteService, Depends(get_invite_service)],
):
    # return await svc.update_status(
    #     invite_id,
    #     TeamInviteStatus.REJECTED,
    #     user,
    # )
    raise NotImplementedHTTPError()
