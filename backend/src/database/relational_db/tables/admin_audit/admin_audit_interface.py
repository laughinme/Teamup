from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ..interfaces import BaseInterface
from .admin_audit_table import AdminAudit


class AdminAuditInterface(BaseInterface[AdminAudit, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(AdminAudit, session)

    async def add_action(
        self,
        *,
        actor_id: UUID | None,
        entity: str,
        entity_id: str,
        action: str,
        payload: dict | None = None,
    ) -> AdminAudit:
        entry = AdminAudit(
            actor_user_id=actor_id,
            entity=entity,
            entity_id=entity_id,
            action=action,
            diff=payload,
        )
        self.session.add(entry)
        await self.session.flush()
        return entry


