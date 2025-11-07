from fastapi import Depends

from database.relational_db import TeamApplicationsInterface, UoW, get_uow

from .application_service import ApplicationService


async def get_application_service(
    uow: UoW = Depends(get_uow),
) -> ApplicationService:
    applications = TeamApplicationsInterface(uow.session)
    return ApplicationService(uow, applications)


