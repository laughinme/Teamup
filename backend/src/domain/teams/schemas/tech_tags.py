from uuid import UUID

from pydantic import BaseModel, Field

from domain.common import TechTagKind


class TechTagModel(BaseModel):
    id: UUID = Field(...)
    slug: str = Field(...)
    name: str = Field(...)
    description: str | None = Field(None)
    kind: TechTagKind = Field(...)
