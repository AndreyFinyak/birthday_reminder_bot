from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import EventType
from app.infrastructure.db.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.db.models.users import User


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user: Mapped["User"] = relationship("User", back_populates="events")

    event_type: Mapped["EventType"] = mapped_column(
        Enum(EventType), nullable=False
    )
    event_date: Mapped[date] = mapped_column(Date, nullable=False)

    chat_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.chat_id"), nullable=False
    )

    owner: Mapped[str] = mapped_column(String(50), nullable=False)
