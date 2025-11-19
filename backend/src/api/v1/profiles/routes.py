from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status, Path
from pydantic import BaseModel

from core.security import auth_user
from database.relational_db import User
from domain.profiles import ProfileModel, ProfileSummary
from domain.common import CursorPage
from domain.errors import NotImplementedHTTPError
# from service.profiles import ProfileService, get_profile_service


router = APIRouter()


@router.get(
    "/",
    response_model=CursorPage[ProfileSummary],
    summary="List profiles. (not implemented yet)",
)
async def list_profiles(
    # service: Annotated[ProfileService, Depends(get_profile_service)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,    
    cursor: Annotated[str | None, Query(description='Opaque cursor')] = None,
):
    # profiles = await service.list_profiles(limit=limit, offset=offset)
    # items = [ProfileSummary.model_validate(profile) for profile in profiles]
    # return CursorPage[ProfileSummary](items=items, next_cursor=None)
    raise NotImplementedHTTPError()


@router.get(
    "/{profile_id}",
    response_model=ProfileModel,
    summary="Get profile by id. (not implemented yet)",
)
async def get_profile(
    profile_id: UUID = Path(..., description="Profile ID"),
    # service: Annotated[ProfileService, Depends(get_profile_service)],
):
    # profile = await service.get_profile(profile_id)
    # if not profile:
    #     raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Profile not found")
    # return ProfileModel.model_validate(profile)
    raise NotImplementedHTTPError()
