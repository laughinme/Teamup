from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from domain.common import (
    Direction,
    ExperienceLevel,
    ProfileVisibility,
    TechTagKind,
    TimeCommitment,
    TimestampModel,
)


class TechTagRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(...)
    slug: str = Field(...)
    name: str = Field(...)
    kind: TechTagKind = Field(...)


class ProfileTechLink(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tag: TechTagRef = Field(...)
    level: int = Field(..., ge=1, le=5)


class ProfileTechInput(BaseModel):
    tag_id: UUID = Field(...)
    level: int = Field(..., ge=1, le=5)


class ProfileModel(TimestampModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(...)
    direction: Direction = Field(...)
    bio: str | None = Field(None)
    experience_level: ExperienceLevel = Field(...)
    achievements: list[str] = Field(default_factory=list)
    languages_spoken: list[str] = Field(default_factory=list)
    preferred_language_codes: list[str] = Field(default_factory=list)
    time_commitment: TimeCommitment = Field(...)
    timezone: str = Field(...)
    preferred_roles: list[str] = Field(default_factory=list)
    visibility: ProfileVisibility = Field(default=ProfileVisibility.PUBLIC)
    tech_stack: list[ProfileTechLink] = Field(default_factory=list)


class ProfileSummary(ProfileModel):
    tech_stack: list[ProfileTechLink] = Field(default_factory=list)


class ProfileUpdate(BaseModel):
    direction: Direction | None = Field(None)
    bio: str | None = Field(None, max_length=2000)
    experience_level: ExperienceLevel | None = Field(None)
    achievements: list[str] | None = Field(None)
    languages_spoken: list[str] | None = Field(None)
    preferred_language_codes: list[str] | None = Field(None)
    time_commitment: TimeCommitment | None = Field(None)
    timezone: str | None = Field(None)
    preferred_roles: list[str] | None = Field(None)
    visibility: ProfileVisibility | None = Field(None)
    tech_stack: list[ProfileTechInput] | None = Field(
        None,
        description="Полный список технологий с уровнем. Оставьте None чтобы не менять стек.",
    )


class ProfileFilters(BaseModel):
    direction: Direction | None = Field(None)
    experience_level: ExperienceLevel | None = Field(None)
    timezone: str | None = Field(None)
    language: str | None = Field(None)
    visibility: ProfileVisibility | None = Field(None)
    search: str | None = Field(None)
    tag_ids: list[UUID] | None = Field(None)
    min_level: Annotated[int | None, Field(None, ge=1, le=5)] = None


class ProfileListResponse(BaseModel):
    items: list[ProfileSummary] = Field(default_factory=list)
    next_cursor: str | None = Field(None)


