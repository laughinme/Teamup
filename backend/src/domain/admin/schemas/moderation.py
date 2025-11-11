from enum import Enum

from pydantic import BaseModel, Field


class AdminExportScope(str, Enum):
    TEAMS = "teams"
    PROFILES = "profiles"
    MEMBERS = "members"
    APPLICATIONS = "applications"


class ModerationActionPayload(BaseModel):
    reason: str | None = Field(None, max_length=2000)
    notes: str | None = Field(None, max_length=2000)


