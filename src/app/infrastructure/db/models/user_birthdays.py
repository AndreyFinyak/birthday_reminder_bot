# birthday.py
from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.models.base import Base


class UserBirthday(Base):
    __tablename__ = "user_birthdays"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    birthday_date: Mapped[date] = mapped_column(Date, nullable=False)
