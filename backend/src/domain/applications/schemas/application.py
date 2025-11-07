from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from domain.common import TimestampModel
from domain.teams import TeamApplicationStatus


class ApplicationModel(TimestampModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(...)
    team_id: UUID = Field(...)
    applicant_id: UUID = Field(...)
    status: TeamApplicationStatus = Field(...)
    message: str | None = Field(None, max_length=2000)


class ApplicationCreate(BaseModel):
    message: str | None = Field(None, max_length=2000)


class ApplicationActionPayload(BaseModel):
    note: str | None = Field(None, max_length=2000)


class ApplicationListResponse(BaseModel):
    items: list[ApplicationModel] = Field(default_factory=list)
    next_cursor: str | None = Field(None)


