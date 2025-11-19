from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.security import auth_user
from database.relational_db import User
from domain.invites import InviteCreate, InviteModel, InviteStatusUpdate
from domain.teams import TeamInviteStatus
from domain.common import CursorPage
from domain.errors import NotImplementedHTTPError
# from service.invites import InviteService, get_invite_service
# from service.teams import TeamService, get_team_service


router = APIRouter()


@router.get(
    "/",
    response_model=CursorPage[InviteModel],
    summary="List invites sent to me. (not implemented yet)",
)
async def list_invites_sent_to_me(
    user: Annotated[User, Depends(auth_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    cursor: Annotated[str | None, Query(description='Opaque cursor')] = None,
    # svc: Annotated[InviteService, Depends(get_invite_service)],
):
    raise NotImplementedHTTPError()


@router.patch(
    "/{invite_id}",
    response_model=InviteModel,
    summary="Update my invite status (accept/reject). (not implemented yet)",
    description="Recipient user can accept or reject the invite. "
                "Expected payload.status is ACCEPTED or REJECTED.",
)
async def update_my_invite_status(
    invite_id: UUID,
    payload: InviteStatusUpdate,
    user: Annotated[User, Depends(auth_user)],
    # svc: Annotated[InviteService, Depends(get_invite_service)],
):
    if payload.status not in [TeamInviteStatus.ACCEPTED, TeamInviteStatus.REJECTED]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Expected status: ACCEPTED or REJECTED")
    # return await svc.update_status(invite_id, payload.status, user, note=payload.note)
    raise NotImplementedHTTPError()
