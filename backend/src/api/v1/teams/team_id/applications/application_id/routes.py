from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from core.security import auth_user
from database.relational_db import User
from domain.applications import ApplicationModel, ApplicationStatusUpdate
from domain.errors import NotImplementedHTTPError
from domain.teams import TeamApplicationStatus
# from service.applications import ApplicationService, get_application_service


router = APIRouter()


@router.patch(
    "/",
    response_model=ApplicationModel,
    summary="Update team application status (accept/reject)",
    description="Team admins can accept/reject applications through this endpoint."
                "Expected payload.status is ACCEPTED or REJECTED, otherwise 400 Bad Request will be raised."
                "User can withdraw their own application only through /users/me/applications/{application_id} endpoint.",
)
async def update_application_status(
    application_id: UUID,
    payload: ApplicationStatusUpdate,
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[ApplicationService, Depends(get_application_service)],
):
    if payload.status not in [TeamApplicationStatus.ACCEPTED, TeamApplicationStatus.REJECTED]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Expected status: ACCEPTED or REJECTED")
    raise NotImplementedHTTPError()
