from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from core.security import auth_user
from database.relational_db import User
from domain.applications import (
    ApplicationModel,
    ApplicationCreate,
)
from domain.errors import NotImplementedHTTPError


router = APIRouter()


@router.post(
    "/",
    response_model=ApplicationModel,
    status_code=status.HTTP_201_CREATED,
    summary="Appeal to join a team",
)
async def create_application(
    team_id: UUID,
    payload: ApplicationCreate,
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[ApplicationService, Depends(get_application_service)],
):
    # application = await service.create_application(
    #     team_id=team_id,
    #     applicant_id=user.id,
    #     payload=payload,
    # )
    # return ApplicationModel.model_validate(application)
    raise NotImplementedHTTPError()
