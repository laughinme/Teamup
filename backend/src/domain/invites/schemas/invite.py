from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from domain.common import TimestampModel
from domain.teams import TeamInviteStatus


class InviteModel(TimestampModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(...)
    team_id: UUID = Field(...)
    invited_user_id: UUID = Field(...)
    invited_by_user_id: UUID = Field(...)
    status: TeamInviteStatus = Field(...)
    message: str | None = Field(None, max_length=2000)
    expires_at: datetime | None = Field(None)


class InviteCreate(BaseModel):
    user_id: UUID = Field(...)
    message: str | None = Field(None, max_length=2000)
    expires_at: datetime | None = Field(None)


class InviteActionPayload(BaseModel):
    note: str | None = Field(None, max_length=2000)
