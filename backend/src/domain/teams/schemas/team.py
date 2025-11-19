from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from domain.common import Direction, ExperienceLevel
from domain.teams import (
    TeamMemberStatus,
    TeamRole,
    TeamStatus,
    TeamVisibility,
    NeedRequirementType,
)
from domain.common import TimestampModel
from .tech_tags import TechTagModel


class TeamNeedTagModel(BaseModel):
    id: UUID = Field(...)
    tag: TechTagModel = Field(...)
    requirement_type: NeedRequirementType = Field(...)

class TeamNeedModel(BaseModel):
    id: UUID = Field(...)
    direction: Direction = Field(...)
    required_level: ExperienceLevel = Field(...)
    must_tags: list[TeamNeedTagModel] = Field(default_factory=list)
    nice_tags: list[TeamNeedTagModel] = Field(default_factory=list)
    slots: int = Field(..., ge=1)
    notes: str | None = Field(None)

class TeamNeedInput(BaseModel):
    direction: Direction = Field(...)
    required_level: ExperienceLevel = Field(...)
    must_tag_ids: list[UUID] = Field(default_factory=list)
    nice_tag_ids: list[UUID] = Field(default_factory=list)
    slots: int = Field(..., ge=1)
    notes: str | None = Field(None)

# class TeamNeedUpdate(BaseModel):
    

class TeamMemberModel(BaseModel):
    user_id: UUID = Field(...)
    role: TeamRole = Field(...)
    status: TeamMemberStatus = Field(...)
    joined_at: datetime | None = Field(None)
    left_at: datetime | None = Field(None)


class TeamModel(TimestampModel):
    id: UUID = Field(...)
    name: str = Field(...)
    description: str | None = Field(None)
    
    # direction: Direction | None = Field(None)
    
    status: TeamStatus = Field(...)
    visibility: TeamVisibility = Field(...)
    max_members: int = Field(...)
    current_members: int = Field(...)
    needs: list[TeamNeedModel] = Field(default_factory=list)
    members: list[TeamMemberModel] = Field(default_factory=list)


class TeamCreate(BaseModel):
    name: str = Field(..., max_length=128)
    description: str | None = Field(None, max_length=2000)
    
    # direction: Direction | None = Field(None)
    
    visibility: TeamVisibility = Field(default=TeamVisibility.PUBLIC)
    max_members: int = Field(5, ge=3, le=5)
    needs: list[TeamNeedInput] = Field(default_factory=list)


class TeamUpdate(BaseModel):
    name: str | None = Field(None, max_length=128)
    description: str | None = Field(None, max_length=2000)
    # direction: Direction | None = Field(None)
    status: TeamStatus | None = Field(None)
    visibility: TeamVisibility | None = Field(None)
    max_members: Annotated[int | None, Field(ge=3, le=5)] = None
    needs: list[TeamNeedInput] | None = Field(None)
