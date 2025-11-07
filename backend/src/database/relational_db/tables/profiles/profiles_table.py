from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
)
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.common import Direction, ExperienceLevel, ProfileVisibility, TimeCommitment

from ..mixins import TimestampMixin
from ..table_base import Base

if TYPE_CHECKING:
    from ..users import User
    from .profile_tech_tags_table import ProfileTechTag


class Profile(TimestampMixin, Base):
    __tablename__ = "profiles"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    direction: Mapped[Direction] = mapped_column(ENUM(Direction), nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    experience_level: Mapped[ExperienceLevel] = mapped_column(
        ENUM(ExperienceLevel), nullable=False
    )
    achievements: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False, default=list)
    languages_spoken: Mapped[list[str]] = mapped_column(
        ARRAY(String(8)), nullable=False, default=list
    )
    preferred_language_codes: Mapped[list[str]] = mapped_column(
        ARRAY(String(8)), nullable=False, default=list
    )
    time_commitment: Mapped[TimeCommitment] = mapped_column(
        ENUM(TimeCommitment), nullable=False
    )
    timezone: Mapped[str] = mapped_column(String(64), nullable=False)
    preferred_roles: Mapped[list[str]] = mapped_column(
        ARRAY(String(32)), nullable=False, default=list
    )
    visibility: Mapped[ProfileVisibility] = mapped_column(
        ENUM(ProfileVisibility), nullable=False, default=ProfileVisibility.PUBLIC
    )
    search_vector: Mapped[str | None] = mapped_column(
        TSVECTOR,
        nullable=True,
    )

    __table_args__ = (
        Index("profiles_visibility_idx", "visibility"),
        Index("profiles_direction_idx", "direction"),
        Index(
            "profiles_search_vector_gin_idx",
            "search_vector",
            postgresql_using="gin",
        ),
    )

    user: Mapped[User] = relationship(
        "User",
        back_populates="profile",
        lazy="selectin",
    )
    tech_links: Mapped[list[ProfileTechTag]] = relationship(
        "ProfileTechTag",
        back_populates="profile",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


__all__ = ["Profile"]

