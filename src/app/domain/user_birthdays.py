from dataclasses import dataclass
from datetime import date


@dataclass
class UserBirthday:
    id: int
    telegram_id: int
    username: str | None
    name: str
    birthday_date: date
