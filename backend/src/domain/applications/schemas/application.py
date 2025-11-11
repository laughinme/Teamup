from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from domain.common import TimestampModel
from domain.teams import TeamApplicationStatus


class ApplicationModel(TimestampModel):
    id: UUID = Field(...)
    team_id: UUID = Field(...)
    applicant_id: UUID = Field(...)
    status: TeamApplicationStatus = Field(...)
    message: str | None = Field(None, max_length=2000)


class ApplicationCreate(BaseModel):
    message: str | None = Field(None, max_length=2000)


class ApplicationActionPayload(BaseModel):
    note: str | None = Field(None, max_length=2000)


class ApplicationStatusUpdate(BaseModel):
    status: TeamApplicationStatus = Field(..., description="New application status")
    note: str | None = Field(None, max_length=2000, description="Optional moderator/applicant note")
