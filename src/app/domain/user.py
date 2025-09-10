from dataclasses import dataclass


@dataclass
class User:
    id: int
    telegram_id: int
    username: str | None
