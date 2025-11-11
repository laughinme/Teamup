from uuid import UUID
from pydantic import BaseModel, Field

from ..enums import FeedEntityType


class FeedItem(BaseModel):
    entity_type: FeedEntityType = Field(...)
    entity_id: UUID = Field(...)
    score: float = Field(...)
    reason: str | None = Field(None)
