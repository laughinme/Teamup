from typing import Annotated

from fastapi import APIRouter, Depends, Query

from domain.teams import TeamModel
from domain.common import CursorPage
from domain.errors import NotImplementedHTTPError
# from service.teams import TeamService, get_team_service


router = APIRouter()

@router.get(
    "/",
    response_model=CursorPage[TeamModel],
    summary="Team catalog. (not implemented yet)",
)
async def list_teams(
    # service: Annotated[TeamService, Depends(get_team_service)],
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    # teams = await service.list_teams(limit=limit, offset=offset)
    # items = [TeamModel.model_validate(team) for team in teams]
    # return CursorPage[TeamModel](items=items, next_cursor=None)
    raise NotImplementedHTTPError()
