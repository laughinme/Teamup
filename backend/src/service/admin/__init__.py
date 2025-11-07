from fastapi import Depends

from database.relational_db import AdminAuditInterface, UoW, get_uow

from .admin_service import AdminService


async def get_admin_service(
    uow: UoW = Depends(get_uow),
) -> AdminService:
    audit = AdminAuditInterface(uow.session)
    return AdminService(uow, audit)


