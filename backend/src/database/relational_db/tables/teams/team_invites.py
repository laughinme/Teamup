from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Uuid, Text, DateTime, Index, text
from sqlalchemy.dialects.postgresql import ENUM

from domain.teams import TeamInviteStatus

from ..table_base import Base
from ..mixins import TimestampMixin

if TYPE_CHECKING:
    from ..users.users_table import User
    from .teams_table import Team
    from .team_memberships import TeamMembership


class TeamInvite(TimestampMixin, Base):
    __tablename__ = "team_invites"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    team_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    invited_user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    invited_by_user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    status: Mapped[TeamInviteStatus] = mapped_column(
        ENUM(TeamInviteStatus), nullable=False, default=TeamInviteStatus.PENDING
    )
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    responded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index(
            "team_invites_unique_pending_idx",
            "team_id",
            "invited_user_id",
            unique=True,
            postgresql_where=text("status = 'PENDING'"),
        ),
    )

    team: Mapped["Team"] = relationship(  # pyright: ignore
        "Team",
        back_populates="invites",
        lazy="selectin",
    )
    invited_user: Mapped["User"] = relationship(  # pyright: ignore
        "User",
        lazy="selectin",
        foreign_keys=[invited_user_id],
    )
    invited_by: Mapped["User"] = relationship(  # pyright: ignore
        "User",
        lazy="selectin",
        foreign_keys=[invited_by_user_id],
    )
    resulting_membership: Mapped["TeamMembership | None"] = relationship(  # pyright: ignore
        "TeamMembership",
        back_populates="invite",
        lazy="selectin",
        uselist=False,
    )
