from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .mixin import UserRelationMixin


class Profile(Base, UserRelationMixin):
    _user_back_populates = 'profile'
    _user_id_unique = True
    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    biography: Mapped[str | None]