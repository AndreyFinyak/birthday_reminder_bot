from dataclasses import dataclass


@dataclass
class User:
    chat_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
