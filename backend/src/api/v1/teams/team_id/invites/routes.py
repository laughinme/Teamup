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


@router.post(
    "/",
    response_model=InviteModel,
    status_code=status.HTTP_201_CREATED,
    summary="Send invite to a user. (not implemented yet)",
)
async def send_invite(
    team_id: UUID,
    payload: InviteCreate,
    user: Annotated[User, Depends(auth_user)],
    # invite_svc: Annotated[InviteService, Depends(get_invite_service)],
    # team_svc: Annotated[TeamService, Depends(get_team_service)],
):
    # team = await team_svc.get_team(team_id)
    # if not team:
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    # if team.created_by_user_id != user.id:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not a team owner")

    # invite = await invite_service.create_invite(
    #     team_id=team_id,
    #     invited_user_id=payload.user_id,
    #     invited_by_user_id=user.id,
    #     payload=payload,
    # )
    # return InviteModel.model_validate(invite)
    raise NotImplementedHTTPError()


@router.get(
    "/",
    response_model=CursorPage[InviteModel],
    summary="List invites. (not implemented yet)",
)
async def list_invites(
    user: Annotated[User, Depends(auth_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    cursor: Annotated[str | None, Query(description='Opaque cursor')] = None,
    # svc: Annotated[InviteService, Depends(get_invite_service)],
):
    raise NotImplementedHTTPError()
