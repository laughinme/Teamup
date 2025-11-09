from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from core.security import auth_user
from database.relational_db import User
from domain.teams import (
    TeamListResponse,
    TeamModel,
)
from service.teams import TeamService, get_team_service


router = APIRouter()

@router.get(
    "/",
    response_model=TeamListResponse,
    summary="Team catalog",
)
async def list_teams(
    service: Annotated[TeamService, Depends(get_team_service)],
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    teams = await service.list_teams(limit=limit, offset=offset)
    items = [TeamModel.model_validate(team) for team in teams]
    return TeamListResponse(items=items, next_cursor=None)
