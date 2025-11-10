from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.security import auth_user
from database.relational_db import User
from domain.applications import (
    ApplicationCreate,
    ApplicationModel,
)
from domain.common import CursorPage
from domain.teams import TeamApplicationStatus
from domain.errors import NotImplementedHTTPError
# from service.applications import ApplicationService, get_application_service


router = APIRouter()


@router.get(
    "/applications",
    response_model=CursorPage[ApplicationModel],
    summary="My applications",
)
async def list_my_applications(
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[ApplicationService, Depends(get_application_service)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    # applications = await service.list_for_user(user_id=user.id, limit=limit, offset=offset)
    # items = [ApplicationModel.model_validate(app) for app in applications]
    # return CursorPage(items=items, next_cursor=None)
    raise NotImplementedHTTPError()


@router.post(
    "/{application_id}/withdraw",
    response_model=ApplicationModel,
    summary="Withdraw application",
)
async def withdraw_application(
    application_id: UUID,
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[ApplicationService, Depends(get_application_service)],
):
    # return await _change_application_status(
    #     application_id,
    #     TeamApplicationStatus.WITHDRAWN,
    #     service,
    #     user,
    # )
    raise NotImplementedHTTPError()


@router.post(
    "/{application_id}/accept",
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
    "/{application_id}/reject",
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
