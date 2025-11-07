from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ..interfaces import BaseInterface
from .notifications_table import Notification


class NotificationsInterface(BaseInterface[Notification, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(Notification, session)


