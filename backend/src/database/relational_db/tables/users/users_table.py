from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Uuid, String, Boolean, DateTime, Text, Index, Integer

from domain.teams import TeamRole

from ..table_base import Base
from ..mixins import TimestampMixin

if TYPE_CHECKING:
    from ..teams import TeamMembership, Team
    from ..profiles import Profile

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), default=uuid4, primary_key=True)
    
    # Credentials
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Profile info
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    language_code: Mapped[str | None] = mapped_column(
        String(2), ForeignKey('languages.code'), nullable=True
    )
    
    # Service
    is_onboarded: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    banned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    auth_version: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default="1"
    )

    __table_args__ = (
        # GIN trigram indexes for fast text search
        Index(
            'users_username_trgm',
            'username',
            postgresql_using='gin',
            postgresql_ops={'username': 'gin_trgm_ops'}
        ),
        Index(
            'users_email_trgm',
            'email',
            postgresql_using='gin',
            postgresql_ops={'email': 'gin_trgm_ops'}
        ),
    )
    
    roles: Mapped[list["Role"]] = relationship(  # pyright: ignore
        "Role",
        secondary="user_roles",
        back_populates="users",
        lazy="selectin",
    )
    profile: Mapped["Profile | None"] = relationship(
        "Profile",
        back_populates="user",
        lazy="selectin",
        uselist=False,
    )
    # notifications: Mapped[list["Notification"]] = relationship(
    #     "Notification",
    #     back_populates="user",
    #     lazy="selectin",
    #     cascade="all, delete-orphan",
    # )
    team: Mapped["Team"] = relationship(
        secondary="team_memberships",
        back_populates="members",
        uselist=False,
        lazy="selectin",
        foreign_keys="[TeamMembership.user_id, TeamMembership.team_id]",
    )
    team_membership: Mapped["TeamMembership"] = relationship( # type: ignore
        "TeamMembership",
        back_populates="user",
        uselist=False,
        lazy="selectin",
        foreign_keys="[TeamMembership.user_id]",
    )
    
    @property
    def team_role(self) -> TeamRole | None:
        return self.team_membership.role if self.team_membership else None
    
    @property
    def role_slugs(self) -> list[str]:
        return [role.slug for role in self.roles]

    def has_roles(self, *slugs: str) -> bool:
        if not slugs:
            return True
        owned = set(self.role_slugs)
        return all(slug in owned for slug in slugs)

    def bump_auth_version(self) -> None:
        self.auth_version = (self.auth_version or 0) + 1
