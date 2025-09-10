from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import EventType
from app.infrastructure.db.models.base import Base
from app.infrastructure.db.models.users import User


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped["EventType"] = mapped_column(
        Enum(EventType), nullable=False
    )
    event_date: Mapped[date] = mapped_column(Date, nullable=False)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="events")
