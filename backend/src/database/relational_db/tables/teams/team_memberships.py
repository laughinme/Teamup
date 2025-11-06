from uuid import UUID
from datetime import datetime, UTC

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Uuid, func, DateTime, Index, text
from sqlalchemy.dialects.postgresql import ENUM

from domain.teams import TeamRole

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
    
    invited_by: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    invited_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), server_default=func.now()
    )

    __table_args__ = (
        Index(
            'unique_team_owner_idx',
            'team_id',
            unique=True,
            postgresql_where=text(f"role = '{TeamRole.OWNER.value.upper()}'")
        ),
    )
    
    user: Mapped["User"] = relationship(back_populates="team_membership", lazy="selectin", foreign_keys=[user_id])  # pyright: ignore
    team: Mapped["Team"] = relationship(  # pyright: ignore
        back_populates="team_memberships",
        lazy="selectin",
    )
