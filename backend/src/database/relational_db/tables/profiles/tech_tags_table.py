from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Index, String, Text, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid

from domain.common import TechTagKind

from ..mixins import TimestampMixin
from ..table_base import Base


class TechTag(TimestampMixin, Base):
    __tablename__ = "tech_tags"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    kind: Mapped[TechTagKind] = mapped_column(ENUM(TechTagKind), nullable=False)

    __table_args__ = (
        Index("tech_tags_kind_idx", "kind"),
    )

    profiles: Mapped[list["ProfileTechTag"]] = relationship(
        "ProfileTechTag",
        back_populates="tech_tag",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ProfileTechTag(TimestampMixin, Base):
    __tablename__ = "profile_tech_tags"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    profile_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    tech_tag_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("tech_tags.id", ondelete="CASCADE"),
        nullable=False,
    )
    level: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint("profile_id", "tech_tag_id", name="profile_tech_tags_unique"),
        CheckConstraint("level BETWEEN 1 AND 5", name="profile_tech_tags_level_range"),
    )

    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="tech_links",
        lazy="selectin",
        primaryjoin="ProfileTechTag.profile_id == Profile.id",
    )
    tech_tag: Mapped[TechTag] = relationship(
        "TechTag",
        back_populates="profiles",
        lazy="selectin",
        primaryjoin="ProfileTechTag.tech_tag_id == TechTag.id",
    )


__all__ = ["TechTag", "ProfileTechTag"]

