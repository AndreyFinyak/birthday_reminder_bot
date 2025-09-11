from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.db.models.events import Event


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    chat_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=True)

    events: Mapped[list["Event"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
