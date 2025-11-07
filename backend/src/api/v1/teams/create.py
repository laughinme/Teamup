from typing import Annotated
from fastapi import APIRouter, Depends

from database.relational_db import User
from domain.teams import TeamModel, TeamCreate
from core.security import auth_user, require
from service.teams import TeamService, get_team_service

router = APIRouter()

@router.post(
    path='/',
    response_model=TeamModel,
    summary='Create a new team'
)
async def create_team(
    payload: TeamCreate,
    user: Annotated[User, Depends(auth_user)],
    svc: Annotated[TeamService, Depends(get_team_service)],
):
    return await svc.create_team(payload, user)
