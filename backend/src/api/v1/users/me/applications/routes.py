from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException, status

from core.security import auth_user
from database.relational_db import User
from domain.applications import ApplicationModel, ApplicationStatusUpdate
from domain.common import CursorPage
from domain.teams import TeamApplicationStatus
from domain.errors import NotImplementedHTTPError
# from service.applications import ApplicationService, get_application_service


router = APIRouter()

@router.get(
    "/",
    response_model=CursorPage[ApplicationModel],
    summary="My applications. (not implemented yet)",
)
async def list_my_applications(
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[ApplicationService, Depends(get_application_service)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    cursor: Annotated[str | None, Query(description='Opaque cursor')] = None,
):
    # applications = await service.list_for_user(user_id=user.id, limit=limit, offset=offset)
    # items = [ApplicationModel.model_validate(app) for app in applications]
    # return CursorPage(items=items, next_cursor=None)
    raise NotImplementedHTTPError()

@router.patch(
    "/{application_id}",
    response_model=ApplicationModel,
    summary="Update user's application status (withdraw). (not implemented yet)",
    description="User can only withdraw their own application through this endpoint."
                "Expected payload.status == WITHDRAWN, otherwise 400 Bad Request will be raised."
                "Team admin can accept/reject applications through /teams/{team_id}/applications/{application_id} endpoint.",
)
async def update_my_application_status(
    application_id: UUID,
    payload: ApplicationStatusUpdate,
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[ApplicationService, Depends(get_application_service)],
):
    if payload.status != TeamApplicationStatus.WITHDRAWN:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Expected status: WITHDRAWN")
    # TODO: Implement withdrawal logic in service layer.
    raise NotImplementedHTTPError()
