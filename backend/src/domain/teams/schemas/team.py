from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from domain.common import Direction, ExperienceLevel
from domain.teams import (
    TeamMemberStatus,
    TeamRole,
    TeamStatus,
    TeamVisibility,
)
from domain.common import TimestampModel


class TeamNeedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(...)
    direction: Direction = Field(...)
    required_level: ExperienceLevel = Field(...)
    must_tag_ids: list[UUID] = Field(default_factory=list)
    nice_tag_ids: list[UUID] = Field(default_factory=list)
    slots: int = Field(..., ge=1)
    notes: str | None = Field(None)


class TeamNeedInput(BaseModel):
    id: UUID | None = Field(None)
    direction: Direction = Field(...)
    required_level: ExperienceLevel = Field(...)
    must_tag_ids: list[UUID] = Field(default_factory=list)
    nice_tag_ids: list[UUID] = Field(default_factory=list)
    slots: int = Field(..., ge=1)
    notes: str | None = Field(None)


class TeamMemberModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID = Field(...)
    role: TeamRole = Field(...)
    status: TeamMemberStatus = Field(...)
    joined_at: datetime | None = Field(None)
    left_at: datetime | None = Field(None)


class TeamModel(TimestampModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(...)
    name: str = Field(...)
    description: str | None = Field(None)
    direction: Direction | None = Field(None)
    status: TeamStatus = Field(...)
    visibility: TeamVisibility = Field(...)
    max_members: int = Field(...)
    current_members: int = Field(...)
    needs: list[TeamNeedModel] = Field(default_factory=list)
    members: list[TeamMemberModel] = Field(default_factory=list)


class TeamCreate(BaseModel):
    name: str = Field(..., max_length=128)
    description: str | None = Field(None, max_length=2000)
    direction: Direction | None = Field(None)
    visibility: TeamVisibility = Field(default=TeamVisibility.PUBLIC)
    max_members: Annotated[int, Field(ge=3, le=5)] = 5
    needs: list[TeamNeedInput] = Field(default_factory=list)


class TeamUpdate(BaseModel):
    name: str | None = Field(None, max_length=128)
    description: str | None = Field(None, max_length=2000)
    direction: Direction | None = Field(None)
    status: TeamStatus | None = Field(None)
    visibility: TeamVisibility | None = Field(None)
    max_members: Annotated[int | None, Field(ge=3, le=5)] = None
    needs: list[TeamNeedInput] | None = Field(None)


class TeamListResponse(BaseModel):
    items: list[TeamModel] = Field(default_factory=list)
    next_cursor: str | None = Field(None)


