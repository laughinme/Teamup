from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, TSVECTOR

from domain.common import Direction, ExperienceLevel, ProfileVisibility, TimeCommitment

from ..mixins import TimestampMixin
from ..table_base import Base

if TYPE_CHECKING:
    from ..users import User
    from .profile_tech_tags import ProfileTechTag


class Profile(TimestampMixin, Base):
    __tablename__ = "profiles"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    direction: Mapped[Direction] = mapped_column(ENUM(Direction), nullable=False, index=True)
    experience_level: Mapped[ExperienceLevel] = mapped_column(
        ENUM(ExperienceLevel), nullable=True
    )
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    achievements: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False, default=list)
    timezone: Mapped[str] = mapped_column(String(64), nullable=True)
    visibility: Mapped[ProfileVisibility] = mapped_column(
        ENUM(ProfileVisibility), nullable=False, default=ProfileVisibility.PUBLIC, index=True
    )
    # time_commitment: Mapped[TimeCommitment] = mapped_column(
    #     ENUM(TimeCommitment), nullable=True
    # )
    # preferred_roles: Mapped[list[str]] = mapped_column(
    #     ARRAY(String(32)), nullable=False, default=list
    # )
    # languages_spoken: Mapped[list[str]] = mapped_column(
    #     ARRAY(String(8)), nullable=False, default=list
    # )
    # preferred_language_codes: Mapped[list[str]] = mapped_column(
    #     ARRAY(String(8)), nullable=False, default=list
    # )
    # search_vector: Mapped[str | None] = mapped_column(
    #     TSVECTOR,
    #     nullable=True,
    # )
    profile_pic_url: Mapped[str | None] = mapped_column(String, nullable=True)

    # __table_args__ = (
    #     Index(
    #         "profiles_search_vector_gin_idx",
    #         "search_vector",
    #         postgresql_using="gin",
    #     ),
    # )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        lazy="selectin",
    )
    tech_links: Mapped[list["ProfileTechTag"]] = relationship(
        "ProfileTechTag",
        back_populates="profile",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
