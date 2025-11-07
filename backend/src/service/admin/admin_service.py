from uuid import UUID

from database.relational_db import AdminAuditInterface, UoW
from domain.admin import AdminExportScope, ModerationActionPayload


class AdminService:
    def __init__(self, uow: UoW, audit: AdminAuditInterface) -> None:
        self.uow = uow
        self.audit = audit

    async def export_scope(self, scope: AdminExportScope) -> bytes:
        # TODO: implement real CSV export streaming
        header = f"scope,{scope.value}\n"
        return header.encode("utf-8")

    async def moderate(
        self,
        entity: str,
        entity_id: UUID,
        action: str,
        payload: ModerationActionPayload,
        *,
        actor_id: UUID | None = None,
    ) -> None:
        await self.audit.add_action(
            actor_id=actor_id,
            entity=entity,
            entity_id=str(entity_id),
            action=action,
            payload=payload.model_dump(exclude_none=True),
        )
        await self.uow.commit()

