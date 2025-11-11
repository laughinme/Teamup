from typing import Annotated
from fastapi import APIRouter, Depends

from database.relational_db import User
from domain.users import UserModel, UserPatch
from domain.profiles import (
    ProfileModel,
    ProfileSummary,
    ProfileUpdate,
    # MeProfileResponse
)
from core.security import auth_user
from service.users import UserService, get_user_service
from domain.errors import NotImplementedHTTPError

router = APIRouter()

@router.get(
    path='/',
    response_model=UserModel,
    summary='Get user account info'
)
async def profile(
    user: Annotated[User, Depends(auth_user)],
    # TODO: Add expandable fields
    # expand: Annotated[list[ExpandUserFields], Query(default_factory=list, description="Fields to expand with in the response")],
    # svc: Annotated[UserService, Depends(get_user_service)],
):
    return user


@router.patch(
    path='/',
    response_model=UserModel,
    summary='Update user info'
)
async def update_profile(
    payload: UserPatch,
    user: Annotated[User, Depends(auth_user)],
    svc: Annotated[UserService, Depends(get_user_service)],
):
    await svc.patch_user(payload, user)
    return user


@router.get(
    "/profile",
    response_model=ProfileModel,
    summary="Get my profile",
)
async def get_my_profile(
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[ProfileService, Depends(get_profile_service)],
):
    # profile = await service.get_profile(user.id)
    # user_model = UserModel.model_validate(user)
    # profile_model = ProfileModel.model_validate(profile) if profile else None
    # return MeProfileResponse(user=user_model, profile=profile_model)
    raise NotImplementedHTTPError()


@router.put(
    "/profile",
    response_model=ProfileModel,
    summary="Update my profile",
)
async def update_my_profile(
    payload: ProfileUpdate,
    user: Annotated[User, Depends(auth_user)],
    # service: Annotated[ProfileService, Depends(get_profile_service)],
):
    # try:
    #     profile = await service.upsert_profile(user.id, payload)
    # except ValueError as exc:
    #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    # return ProfileModel.model_validate(profile)
    raise NotImplementedHTTPError()
