from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from core.security import auth_user
from database.relational_db import User
from domain.teams import (
    TeamModel,
    TeamNeedInput,
    TeamUpdate,
)
from domain.errors import NotImplementedHTTPError
# from service.teams import TeamService, get_team_service


router = APIRouter()

@router.get(
    "/",
    response_model=TeamModel,
    summary="Get team details",
)
async def get_team(
    team_id: UUID,
    # service: Annotated[TeamService, Depends(get_team_service)],
):
    # team = await service.get_team(team_id)
    # if not team:
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    # return TeamModel.model_validate(team)
    raise NotImplementedHTTPError()


@router.put(
    "/",
    response_model=TeamModel,
    summary="Update team",
)
async def update_team(
    team_id: UUID,
    payload: TeamUpdate,
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[TeamService, Depends(get_team_service)],
):
    # team = await service.get_team(team_id)
    # if not team:
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    # if team.created_by_user_id != user.id:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not a team owner")
    # team = await service.update_team(team=team, payload=payload)
    # return TeamModel.model_validate(team)
    raise NotImplementedHTTPError()


@router.post(
    "/needs",
    response_model=TeamModel,
    summary="Add team need",
)
async def add_team_need(
    team_id: UUID,
    payload: TeamNeedInput,
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[TeamService, Depends(get_team_service)],
):
    # team = await service.get_team(team_id)
    # if not team:
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    # if team.created_by_user_id != user.id:
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not a team owner")

    # existing_inputs = [
    #     TeamNeedInput(
    #         id=need.id,
    #         direction=need.direction,
    #         required_level=need.required_level,
    #         must_tag_ids=need.must_tag_ids,
    #         nice_tag_ids=need.nice_tag_ids,
    #         slots=need.slots,
    #         notes=need.notes,
    #     )
    #     for need in team.needs
    # ]
    # existing_inputs.append(payload)
    # team = await service.update_team(
    #     team=team,
    #     payload=TeamUpdate(needs=existing_inputs),
    # )
    # return TeamModel.model_validate(team)
    raise NotImplementedHTTPError()
