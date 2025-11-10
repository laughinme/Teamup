from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from core.security import auth_user
from database.relational_db import User
from domain.applications import ApplicationModel
from domain.common import CursorPage
from domain.errors import NotImplementedHTTPError
# from service.applications import ApplicationService, get_application_service


router = APIRouter()


@router.post(
    "/accept",
    response_model=ApplicationModel,
    summary="Accept team application",
)
async def accept_application(
    application_id: UUID,
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[ApplicationService, Depends(get_application_service)],
):
    # return await service.change_application_status(
    #     application_id,
    #     TeamApplicationStatus.ACCEPTED,
    #     service,
    #     user,
    # )
    raise NotImplementedHTTPError()


@router.post(
    "/reject",
    response_model=ApplicationModel,
    summary="Reject team application",
)
async def reject_application(
    application_id: UUID,
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[ApplicationService, Depends(get_application_service)],
):
    # return await _change_application_status(
    #     application_id,
    #     TeamApplicationStatus.REJECTED,
    #     service,
    #     user,
    # )
    raise NotImplementedHTTPError()
