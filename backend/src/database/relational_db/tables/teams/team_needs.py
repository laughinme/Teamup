from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text, Uuid, and_
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.common import Direction, ExperienceLevel
from domain.teams import NeedRequirementType

from ..mixins import TimestampMixin
from ..table_base import Base

if TYPE_CHECKING:
    from .team_needs import TeamNeed
    from .tech_tags_table import TechTag

class TeamNeedTag(TimestampMixin, Base):
    __tablename__ = "team_need_tags"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    
    requirement_type: Mapped[NeedRequirementType] = mapped_column(ENUM(NeedRequirementType), nullable=False)
    need_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("team_needs.id", ondelete="CASCADE"), nullable=False
    )
    tag_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tech_tags.id", ondelete="CASCADE"), nullable=False
    )
    need: Mapped["TeamNeed"] = relationship(
        "TeamNeed",
        lazy="selectin",
    )
    tag: Mapped["TechTag"] = relationship(
        "TechTag",
        lazy="selectin",
    )


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
    slots: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    team: Mapped["Team"] = relationship(  # pyright: ignore
        "Team",
        back_populates="needs",
        lazy="selectin",
    )
    must_tags: Mapped[list["TeamNeedTag"]] = relationship(
        "TeamNeedTag",
        primaryjoin=lambda: and_(
            TeamNeed.id == TeamNeedTag.need_id,
            TeamNeedTag.requirement_type == NeedRequirementType.MUST,
        ),
        back_populates="need",
        lazy="selectin",
    )
    nice_tags: Mapped[list["TeamNeedTag"]] = relationship(
        "TeamNeedTag",
        primaryjoin=lambda: and_(
            TeamNeed.id == TeamNeedTag.need_id,
            TeamNeedTag.requirement_type == NeedRequirementType.NICE,
        ),
        back_populates="need",
        lazy="selectin",
    )
