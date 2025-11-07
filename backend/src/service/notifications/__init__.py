from fastapi import Depends

from database.relational_db import NotificationsInterface, UoW, get_uow

from .notification_service import NotificationService


async def get_notification_service(
    uow: UoW = Depends(get_uow),
) -> NotificationService:
    notifications = NotificationsInterface(uow.session)
    return NotificationService(uow, notifications)


