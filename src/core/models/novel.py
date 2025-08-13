import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, text

from core.models import Base
from core.models.mixins.id_pk_int_mixin import IdIntPkMixin


class Novel(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(nullable=False)
    obj_cover_name: Mapped[uuid.UUID | None] = mapped_column(nullable=True)

    __table_args__ = (
        Index(
            "ix_novel_title_trgm",
            text("lower(title)"),
            postgresql_using="gin",
            postgresql_ops={"lower(title)": "gin_trgm_ops"},
        ),
    )

    def __repr__(self):
        return f"Novel(title: {self.title})"
