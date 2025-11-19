from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status, Path
from pydantic import BaseModel

from core.security import auth_user
from domain.common import CursorPage
from domain.teams import TechTagModel
from service.teams import TeamService, get_team_service


router = APIRouter()


@router.get(
    "/tech-tags",
    response_model=CursorPage[TechTagModel],
    summary="List tech tags. Supports text search.",
)
async def list_tech_tags(
    service: Annotated[TeamService, Depends(get_team_service)],
    q: Annotated[str, Query(description='Text search query')] = "",
    limit: Annotated[int, Query(ge=1, le=100)] = 20,    
    cursor: Annotated[str | None, Query(description='Opaque cursor')] = None,
):
    tech_tags = await service.list_tech_tags(query=q, limit=limit, cursor=cursor)
    items = [TechTagModel.model_validate(tech_tag) for tech_tag in tech_tags]
    return CursorPage[TechTagModel](items=items, cursor_info=cursor_info)
