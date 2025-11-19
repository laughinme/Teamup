from uuid import UUID
from datetime import datetime, UTC

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Uuid, func, DateTime, Index, text
from sqlalchemy.dialects.postgresql import ENUM

from domain.teams import TeamRole, TeamMembershipOrigin

from ..table_base import Base
from ..mixins import TimestampMixin


class TeamMembership(TimestampMixin, Base):
    __tablename__ = "team_memberships"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True, unique=True
    )
    team_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )

    role: Mapped[TeamRole] = mapped_column(ENUM(TeamRole), nullable=False, default=TeamRole.MEMBER)
    origin: Mapped[TeamMembershipOrigin] = mapped_column(
        ENUM(TeamMembershipOrigin), nullable=False, default=TeamMembershipOrigin.APPLICATION
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), server_default=func.now()
    )
    source_invite_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("team_invites.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )
    source_application_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("team_applications.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )
    added_by_user_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    
    # status: Mapped[TeamMemberStatus] = mapped_column(
    #     ENUM(TeamMemberStatus), nullable=False, default=TeamMemberStatus.ACCEPTED
    # )
    # left_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index(
            'unique_team_owner_idx',
            'team_id',
            unique=True,
            postgresql_where=text(f"role = '{TeamRole.OWNER.value.upper()}'")
        ),
    )

    user: Mapped["User"] = relationship(  # pyright: ignore
        "User",
        back_populates="team_membership",
        lazy="selectin",
        foreign_keys=[user_id],
        overlaps="team",
    )
    team: Mapped["Team"] = relationship(  # pyright: ignore
        back_populates="team_memberships",
        lazy="selectin",
        overlaps="members",
    )
    invite: Mapped["TeamInvite | None"] = relationship(  # pyright: ignore
        "TeamInvite",
        back_populates="resulting_membership",
        lazy="selectin",
        foreign_keys=[source_invite_id],
    )
    application: Mapped["TeamApplication | None"] = relationship(  # pyright: ignore
        "TeamApplication",
        back_populates="resulting_membership",
        lazy="selectin",
        foreign_keys=[source_application_id],
    )
    added_by: Mapped["User | None"] = relationship(  # pyright: ignore
        "User",
        lazy="selectin",
        foreign_keys=[added_by_user_id],
    )
