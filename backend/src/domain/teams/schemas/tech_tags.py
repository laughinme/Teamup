from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from domain.common import TechTagKind


class TechTagModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(...)
    slug: str = Field(...)
    name: str = Field(...)
    description: str | None = Field(None)
    kind: TechTagKind = Field(...)
