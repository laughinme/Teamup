from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Uuid, Text, DateTime, Index, text
from sqlalchemy.dialects.postgresql import ENUM

from domain.teams import TeamApplicationStatus

from ..table_base import Base
from ..mixins import TimestampMixin


class TeamApplication(TimestampMixin, Base):
    __tablename__ = "team_applications"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    team_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    applicant_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    status: Mapped[TeamApplicationStatus] = mapped_column(
        ENUM(TeamApplicationStatus), nullable=False, default=TeamApplicationStatus.PENDING
    )
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_by_user_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index(
            "team_applications_unique_pending_idx",
            "team_id",
            "applicant_id",
            unique=True,
            postgresql_where=text("status = 'PENDING'"),
        ),
    )

    team: Mapped["Team"] = relationship(  # pyright: ignore
        "Team",
        back_populates="applications",
        lazy="selectin",
    )
    applicant: Mapped["User"] = relationship(  # pyright: ignore
        "User",
        lazy="selectin",
        foreign_keys=[applicant_id],
    )
    reviewed_by: Mapped["User | None"] = relationship(  # pyright: ignore
        "User",
        lazy="selectin",
        foreign_keys=[reviewed_by_user_id],
    )
    resulting_membership: Mapped["TeamMembership | None"] = relationship(  # pyright: ignore
        "TeamMembership",
        back_populates="application",
        lazy="selectin",
        uselist=False,
    )
