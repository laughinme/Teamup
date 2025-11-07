from __future__ import annotations

from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlalchemy import select

from database.relational_db import (
    TeamApplication,
    TeamApplicationsInterface,
    UoW,
)
from domain.applications import ApplicationCreate
from domain.teams import TeamApplicationStatus


class ApplicationService:
    def __init__(self, uow: UoW, applications: TeamApplicationsInterface) -> None:
        self.uow = uow
        self.applications = applications

    async def get_application(self, application_id: UUID) -> TeamApplication | None:
        return await self.applications.get_by_id(application_id)

    async def create_application(
        self,
        *,
        team_id: UUID,
        applicant_id: UUID,
        payload: ApplicationCreate,
    ) -> TeamApplication:
        application = TeamApplication(
            id=uuid4(),
            team_id=team_id,
            applicant_id=applicant_id,
            message=payload.message,
            status=TeamApplicationStatus.PENDING,
        )
        application = await self.applications.add(application)
        await self.uow.commit()
        await self.uow.session.refresh(application)
        return application

    async def list_for_user(
        self,
        *,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> list[TeamApplication]:
        stmt = (
            select(TeamApplication)
            .where(TeamApplication.applicant_id == user_id)
            .limit(limit)
            .offset(offset)
            .order_by(TeamApplication.created_at.desc())
        )
        result = await self.uow.session.scalars(stmt)
        return result.unique().all()

    async def update_status(
        self,
        application: TeamApplication,
        status: TeamApplicationStatus,
        *,
        reviewer_id: UUID | None = None,
    ) -> TeamApplication:
        application.status = status
        application.reviewed_by_user_id = reviewer_id
        application.reviewed_at = datetime.now(UTC)
        await self.uow.commit()
        await self.uow.session.refresh(application)
        return application


