from uuid import UUID, uuid4

from sqlalchemy import String, Text, Index
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid

from domain.common import TechTagKind

from ..mixins import TimestampMixin
from ..table_base import Base


class TechTag(TimestampMixin, Base):
    __tablename__ = "tech_tags"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    slug: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    kind: Mapped[TechTagKind] = mapped_column(ENUM(TechTagKind), nullable=False, index=True)

    __table_args__ = (
        # GIN trigram indices for fast text search
        Index(
            "tech_tags_slug_trgm",
            "slug",
            postgresql_using="gin",
            postgresql_ops={"slug": "gin_trgm_ops"},
        ),
        Index(
            "tech_tags_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )
