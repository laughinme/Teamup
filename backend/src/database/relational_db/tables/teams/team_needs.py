from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, Text, Uuid
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.common import Direction, ExperienceLevel

from ..mixins import TimestampMixin
from ..table_base import Base


class TeamNeed(TimestampMixin, Base):
    __tablename__ = "team_needs"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    team_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    direction: Mapped[Direction] = mapped_column(ENUM(Direction), nullable=False)
    required_level: Mapped[ExperienceLevel] = mapped_column(
        ENUM(ExperienceLevel), nullable=False
    )
    must_tag_ids: Mapped[list[UUID]] = mapped_column(
        ARRAY(Uuid(as_uuid=True)), nullable=False, default=list
    )
    nice_tag_ids: Mapped[list[UUID]] = mapped_column(
        ARRAY(Uuid(as_uuid=True)), nullable=False, default=list
    )
    slots: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    team: Mapped["Team"] = relationship(
        "Team",
        back_populates="needs",
        lazy="selectin",
    )


__all__ = ["TeamNeed"]

