from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from core.security import auth_user
from database.relational_db import User
from domain.applications import ApplicationModel
from domain.common import CursorPage
from domain.errors import NotImplementedHTTPError
# from service.applications import ApplicationService, get_application_service


router = APIRouter()

@router.get(
    "/",
    response_model=CursorPage[ApplicationModel],
    summary="My applications",
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
