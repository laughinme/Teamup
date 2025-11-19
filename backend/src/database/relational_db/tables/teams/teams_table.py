from uuid import UUID, uuid4
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Uuid, String, Text, Index, Integer, and_, CheckConstraint
from sqlalchemy.dialects.postgresql import ENUM, ARRAY
from sqlalchemy.ext.hybrid import hybrid_property

from domain.teams import TeamStatus, TeamVisibility
# from domain.common import Direction

from .team_memberships import TeamMembership
from .team_needs import TeamNeed
from ..team_requests import TeamInvite, TeamApplication
from ..table_base import Base
from ..mixins import TimestampMixin


class Team(TimestampMixin, Base):
    __tablename__ = "teams"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), default=uuid4, primary_key=True)
    created_by_user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # directions: Mapped[list[Direction]] = mapped_column(ARRAY(ENUM(Direction)), nullable=False, default=list)
    
    max_members: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    current_members: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    status: Mapped[TeamStatus] = mapped_column(ENUM(TeamStatus), nullable=False, default=TeamStatus.DRAFT)
    visibility: Mapped[TeamVisibility] = mapped_column(ENUM(TeamVisibility), nullable=False, default=TeamVisibility.PUBLIC)
    
    
    @hybrid_property
    def is_available(self) -> bool:
        return (
            self.status == TeamStatus.RECRUITING and
            self.visibility == TeamVisibility.PUBLIC
        )
    
    @is_available.expression
    @classmethod
    def is_available_expr(cls):
        return and_(cls.status == TeamStatus.RECRUITING, cls.visibility == TeamVisibility.PUBLIC)

    __table_args__ = (
        # Index('teams_is_available_idx', 'is_available'),
        CheckConstraint(
            'max_members >= current_members AND max_members > 0 AND max_members <= 5',
            name='max_members_check'
        ),
        # Index('teams_direction_idx', 'direction'),
    )
    
    created_by: Mapped["User"] = relationship(  # pyright: ignore
        "User",
        lazy="selectin",
        foreign_keys=[created_by_user_id],
    )
    team_memberships: Mapped[list["TeamMembership"]] = relationship(
        back_populates="team",
        lazy="selectin",
        foreign_keys=[TeamMembership.team_id],
        # overlaps="team,members",
    )
    members: Mapped[list["User"]] = relationship(   # pyright: ignore
        "User",
        secondary="team_memberships",
        back_populates="team",
        lazy="selectin",
        uselist=True,
        foreign_keys="[TeamMembership.team_id, TeamMembership.user_id]",
    )
    invites: Mapped[list["TeamInvite"]] = relationship(  # pyright: ignore
        "TeamInvite",
        back_populates="team",
        lazy="selectin",
        foreign_keys=[TeamInvite.team_id],
    )
    applications: Mapped[list["TeamApplication"]] = relationship(  # pyright: ignore
        "TeamApplication",
        back_populates="team",
        lazy="selectin",
        foreign_keys=[TeamApplication.team_id],
    )
    needs: Mapped[list[TeamNeed]] = relationship(
        "TeamNeed",
        back_populates="team",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
