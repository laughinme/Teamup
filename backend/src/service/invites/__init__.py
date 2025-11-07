from fastapi import Depends

from database.relational_db import TeamInvitesInterface, UoW, get_uow

from .invite_service import InviteService


async def get_invite_service(
    uow: UoW = Depends(get_uow),
) -> InviteService:
    invites = TeamInvitesInterface(uow.session)
    return InviteService(uow, invites)


