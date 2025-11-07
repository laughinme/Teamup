from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from core.security import auth_user
from database.relational_db import User
from domain.profiles import (
    ProfileListResponse,
    ProfileModel,
    ProfileSummary,
    ProfileUpdate,
)
from domain.users import UserModel
from service.profiles import ProfileService, get_profile_service


router = APIRouter(prefix="/profiles", tags=["profiles"])


class MeProfileResponse(BaseModel):
    user: UserModel
    profile: ProfileModel | None


@router.get("/me", response_model=MeProfileResponse, summary="Получить свой профиль")
async def get_my_profile(
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[ProfileService, Depends(get_profile_service)],
):
    profile = await service.get_profile(user.id)
    user_model = UserModel.model_validate(user)
    profile_model = ProfileModel.model_validate(profile) if profile else None
    return MeProfileResponse(user=user_model, profile=profile_model)


@router.put(
    "/me",
    response_model=ProfileModel,
    summary="Обновить профиль",
)
async def update_my_profile(
    payload: ProfileUpdate,
    user: Annotated[User, Depends(auth_user)],
    service: Annotated[ProfileService, Depends(get_profile_service)],
):
    try:
        profile = await service.upsert_profile(user.id, payload)
    except ValueError as exc:  # pragma: no cover - валидация создаваемых профилей
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return ProfileModel.model_validate(profile)


@router.get(
    "",
    response_model=ProfileListResponse,
    summary="Список профилей участников",
)
async def list_profiles(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    service: Annotated[ProfileService, Depends(get_profile_service)] = Depends(),
):
    profiles = await service.list_profiles(limit=limit, offset=offset)
    items = [ProfileSummary.model_validate(profile) for profile in profiles]
    return ProfileListResponse(items=items, next_cursor=None)


@router.get(
    "/{profile_id}",
    response_model=ProfileModel,
    summary="Получить профиль по идентификатору",
)
async def get_profile(
    profile_id: UUID,
    service: Annotated[ProfileService, Depends(get_profile_service)],
):
    profile = await service.get_profile(profile_id)
    if not profile:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return ProfileModel.model_validate(profile)
