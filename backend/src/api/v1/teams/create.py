from typing import Annotated
from fastapi import APIRouter, Depends

from database.relational_db import User
from domain.teams import TeamModel, TeamCreate
from domain.errors import NotImplementedHTTPError
from core.security import auth_user
# from service.teams import TeamService, get_team_service

router = APIRouter()

@router.post(
    "/",
    response_model=TeamModel,
    status_code=201,
    summary="Create a new team",
)
async def create_team(
    payload: TeamCreate,
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[TeamService, Depends(get_team_service)],
):
    # team = await service.create_team(owner_id=user.id, payload=payload)
    # return team
    raise NotImplementedError()
