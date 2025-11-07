from __future__ import annotations

from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import select

from database.relational_db import Notification, NotificationsInterface, UoW
from domain.notifications import NotificationMarkRead


class NotificationService:
    def __init__(self, uow: UoW, notifications: NotificationsInterface) -> None:
        self.uow = uow
        self.notifications = notifications

    async def get_notification(self, notification_id: UUID) -> Notification | None:
        return await self.notifications.get_by_id(notification_id)

    async def list_for_user(
        self,
        *,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.uow.session.scalars(stmt)
        return result.unique().all()

    async def mark_read(
        self,
        notification: Notification,
        payload: NotificationMarkRead,
    ) -> Notification:
        notification.read_at = datetime.now(UTC) if payload.read else None
        await self.uow.commit()
        await self.uow.session.refresh(notification)
        return notification


