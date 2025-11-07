from __future__ import annotations

from io import BytesIO
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from starlette.responses import StreamingResponse

from core.security import auth_user
from database.relational_db import User
from domain.admin import AdminExportScope, ModerationActionPayload
from service.admin import AdminService, get_admin_service


router = APIRouter(prefix="/admin", tags=["admin"])


def _ensure_admin(user: User) -> None:
    if not user.has_roles("admin"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Admin role required")


@router.get(
    "/export.csv",
    summary="Экспорт CSV",
)
async def export_csv(
    scope: Annotated[AdminExportScope, Query()],
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[AdminService, Depends(get_admin_service)],
):
    _ensure_admin(user)
    content = await service.export_scope(scope)
    buffer = BytesIO(content)
    headers = {"Content-Disposition": f"attachment; filename={scope.value}.csv"}
    return StreamingResponse(buffer, media_type="text/csv", headers=headers)


@router.post(
    "/moderation/{entity}/{entity_id}/{action}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Модерация сущностей",
)
async def moderate_entity(
    entity: str,
    entity_id: UUID,
    action: Annotated[str, Path(pattern="^(hide|unhide|ban)$")],
    payload: ModerationActionPayload,
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[AdminService, Depends(get_admin_service)],
):
    _ensure_admin(user)
    await service.moderate(
        entity=entity,
        entity_id=entity_id,
        action=action,
        payload=payload,
        actor_id=user.id,
    )
    return {"status": "accepted"}


