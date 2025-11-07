from __future__ import annotations

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class FeedEntityType(str, Enum):
    TEAM = "team"
    PROFILE = "profile"


class FeedItem(BaseModel):
    entity_type: FeedEntityType = Field(...)
    entity_id: UUID = Field(...)
    score: float = Field(...)
    reason: str | None = Field(None)


class FeedResponse(BaseModel):
    items: list[FeedItem] = Field(default_factory=list)


