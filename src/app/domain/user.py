from dataclasses import dataclass


@dataclass
class User:
    id: int
    chat_id: int
    username: str | None
