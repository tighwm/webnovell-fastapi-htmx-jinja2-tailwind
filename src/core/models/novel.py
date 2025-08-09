from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, text

from core.models import Base
from core.models.mixins.id_pk_int_mixin import IdIntPkMixin


class Novel(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(nullable=False)

    __table_args__ = (
        Index(
            "ix_novel_titles_search",
            text("to_tsvector('russian'::regconfig, title)"),
            postgresql_using="gin",
        ),
    )
