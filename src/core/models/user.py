from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.id_pk_int_mixin import IdIntPkMixin

if TYPE_CHECKING:
    from core.models import UserSession


class User(Base, IdIntPkMixin):
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    user_sessions: Mapped[list["UserSession"]] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.id}"
