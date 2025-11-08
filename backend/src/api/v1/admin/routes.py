from io import BytesIO
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from starlette.responses import StreamingResponse

from core.security import auth_user, require
from database.relational_db import User
from domain.admin import AdminExportScope, ModerationActionPayload
# from service.admin import AdminService, get_admin_service


router = APIRouter()

@router.get(
    "/export.csv",
    summary="CSV export",
    response_class=StreamingResponse,
)
async def export_csv(
    _: Annotated[None, Depends(require("admin"))],
    scope: Annotated[AdminExportScope, Query()],
    # service: Annotated[AdminService, Depends(get_admin_service)],
):
    # content = await service.export_scope(scope)
    # buffer = BytesIO(content)
    # headers = {"Content-Disposition": f"attachment; filename={scope.value}.csv"}
    # return StreamingResponse(buffer, media_type="text/csv", headers=headers)
    return StreamingResponse(iter([]), media_type="text/csv")


@router.post(
    "/moderation/{entity}/{entity_id}/{action}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Entity moderation",
)
async def moderate_entity(
    entity: str,
    entity_id: UUID,
    action: Annotated[str, Path(pattern="^(hide|unhide|ban)$")],
    payload: ModerationActionPayload,
    user: Annotated[User, Depends(auth_user)],
    _: Annotated[None, Depends(require("admin"))],
    # service: Annotated[AdminService, Depends(get_admin_service)],
):
    # await service.moderate(
    #     entity=entity,
    #     entity_id=entity_id,
    #     action=action,
    #     payload=payload,
    #     actor_id=user.id,
    # )
    return {"status": "accepted"}
