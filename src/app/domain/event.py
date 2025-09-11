from dataclasses import dataclass
from datetime import date

from app.domain.enums import EventType


@dataclass
class Event:
    chat_id: int
    event_type: EventType
    event_date: date
    owner: str
