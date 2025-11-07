from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.security import auth_user
from database.relational_db import User
from domain.teams import (
    TeamCreate,
    TeamListResponse,
    TeamModel,
    TeamNeedInput,
    TeamUpdate,
)
from service.teams import TeamService, get_team_service


router = APIRouter(prefix="/teams", tags=["teams"])


@router.post(
    "",
    response_model=TeamModel,
    status_code=status.HTTP_201_CREATED,
    summary="Создать команду",
)
async def create_team(
    payload: TeamCreate,
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[TeamService, Depends(get_team_service)],
):
    team = await service.create_team(owner_id=user.id, payload=payload)
    return TeamModel.model_validate(team)


@router.get(
    "",
    response_model=TeamListResponse,
    summary="Каталог команд",
)
async def list_teams(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    service: Annotated[TeamService, Depends(get_team_service)] = Depends(),
):
    teams = await service.list_teams(limit=limit, offset=offset)
    items = [TeamModel.model_validate(team) for team in teams]
    return TeamListResponse(items=items, next_cursor=None)


@router.get(
    "/{team_id}",
    response_model=TeamModel,
    summary="Подробности команды",
)
async def get_team(
    team_id: UUID,
    service: Annotated[TeamService, Depends(get_team_service)],
):
    team = await service.get_team(team_id)
    if not team:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    return TeamModel.model_validate(team)


@router.put(
    "/{team_id}",
    response_model=TeamModel,
    summary="Обновить команду",
)
async def update_team(
    team_id: UUID,
    payload: TeamUpdate,
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[TeamService, Depends(get_team_service)],
):
    team = await service.get_team(team_id)
    if not team:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    if team.created_by_user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not a team owner")
    team = await service.update_team(team=team, payload=payload)
    return TeamModel.model_validate(team)


@router.post(
    "/{team_id}/needs",
    response_model=TeamModel,
    summary="Добавить слот команды",
)
async def add_team_need(
    team_id: UUID,
    payload: TeamNeedInput,
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[TeamService, Depends(get_team_service)],
):
    team = await service.get_team(team_id)
    if not team:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")
    if team.created_by_user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not a team owner")

    existing_inputs = [
        TeamNeedInput(
            id=need.id,
            direction=need.direction,
            required_level=need.required_level,
            must_tag_ids=need.must_tag_ids,
            nice_tag_ids=need.nice_tag_ids,
            slots=need.slots,
            notes=need.notes,
        )
        for need in team.needs
    ]
    existing_inputs.append(payload)
    team = await service.update_team(
        team=team,
        payload=TeamUpdate(needs=existing_inputs),
    )
    return TeamModel.model_validate(team)


