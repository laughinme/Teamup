from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import JSON, String, Text, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..mixins import TimestampMixin
from ..table_base import Base


class AdminAudit(TimestampMixin, Base):
    __tablename__ = "admin_audit"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    actor_user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    entity: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(64), nullable=False)
    diff: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    actor: Mapped["User | None"] = relationship(
        "User",
        lazy="selectin",
        foreign_keys=[actor_user_id],
    )


__all__ = ["AdminAudit"]

