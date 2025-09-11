from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import EventType
from app.infrastructure.db.models.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    event_type: Mapped["EventType"] = mapped_column(
        Enum(EventType), nullable=False
    )
    event_date: Mapped[date] = mapped_column(Date, nullable=False)

    chat_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.chat_id"), nullable=False
    )

    owner: Mapped[str] = mapped_column(String(50), nullable=False)
