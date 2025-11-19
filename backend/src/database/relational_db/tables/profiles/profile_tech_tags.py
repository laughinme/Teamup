from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid

if TYPE_CHECKING:
    from ..teams import TechTag
    from ..profiles import Profile

from ..mixins import TimestampMixin
from ..table_base import Base


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
    )
    tech_tag: Mapped["TechTag"] = relationship(
        "TechTag",
        lazy="selectin",
    )
