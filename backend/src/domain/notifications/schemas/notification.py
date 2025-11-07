from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from domain.common import TimestampModel


class NotificationModel(TimestampModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(...)
    user_id: UUID = Field(...)
    kind: str = Field(...)
    payload: dict = Field(default_factory=dict)
    read_at: datetime | None = Field(None)


class NotificationListResponse(BaseModel):
    items: list[NotificationModel] = Field(default_factory=list)
    unread_count: int = Field(0)


class NotificationMarkRead(BaseModel):
    read: bool = Field(True)


