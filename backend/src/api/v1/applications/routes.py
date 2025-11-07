from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.security import auth_user
from database.relational_db import User
from domain.applications import (
    ApplicationCreate,
    ApplicationListResponse,
    ApplicationModel,
)
from domain.teams import TeamApplicationStatus
from service.applications import ApplicationService, get_application_service


router = APIRouter(prefix="", tags=["applications"])


@router.post(
    "/teams/{team_id}/applications",
    response_model=ApplicationModel,
    status_code=status.HTTP_201_CREATED,
    summary="Подать заявку в команду",
)
async def create_application(
    team_id: UUID,
    payload: ApplicationCreate,
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[ApplicationService, Depends(get_application_service)],
):
    application = await service.create_application(
        team_id=team_id,
        applicant_id=user.id,
        payload=payload,
    )
    return ApplicationModel.model_validate(application)


@router.get(
    "/me/applications",
    response_model=ApplicationListResponse,
    summary="Мои заявки",
)
async def list_my_applications(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    user: Annotated[User, Depends(auth_user)] = Depends(),
    service: Annotated[ApplicationService, Depends(get_application_service)] = Depends(),
):
    applications = await service.list_for_user(user_id=user.id, limit=limit, offset=offset)
    items = [ApplicationModel.model_validate(app) for app in applications]
    return ApplicationListResponse(items=items, next_cursor=None)


async def _change_application_status(
    application_id: UUID,
    status_target: TeamApplicationStatus,
    service: ApplicationService,
    user: User,
) -> ApplicationModel:
    application = await service.get_application(application_id)
    if not application:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Application not found")
    if application.applicant_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not an applicant")
    application = await service.update_status(application, status_target, reviewer_id=user.id)
    return ApplicationModel.model_validate(application)


@router.post(
    "/applications/{application_id}/withdraw",
    response_model=ApplicationModel,
    summary="Отозвать заявку",
)
async def withdraw_application(
    application_id: UUID,
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[ApplicationService, Depends(get_application_service)],
):
    return await _change_application_status(
        application_id,
        TeamApplicationStatus.WITHDRAWN,
        service,
        user,
    )


@router.post(
    "/applications/{application_id}/accept",
    response_model=ApplicationModel,
    summary="Принять предложение команды",
)
async def accept_application(
    application_id: UUID,
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[ApplicationService, Depends(get_application_service)],
):
    return await _change_application_status(
        application_id,
        TeamApplicationStatus.ACCEPTED,
        service,
        user,
    )


@router.post(
    "/applications/{application_id}/reject",
    response_model=ApplicationModel,
    summary="Отклонить предложение команды",
)
async def reject_application(
    application_id: UUID,
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[ApplicationService, Depends(get_application_service)],
):
    return await _change_application_status(
        application_id,
        TeamApplicationStatus.REJECTED,
        service,
        user,
    )


