import datetime

from app.domain.event import Event, EventType
from app.infrastructure.db.repository import EventRepository
from app.infrastructure.event_tracker import BirthdayScheduler


class EventService:
    def __init__(
        self,
        event_repository: EventRepository,
        birthday_scheduler: BirthdayScheduler,
    ):
        self.event_repository = event_repository
        self.birthday_scheduler = birthday_scheduler

    async def start_scheduler(self) -> None:
        notification_time = datetime.time(hour=9, minute=0)
        await self.birthday_scheduler.start(
            notification_time=notification_time
        )

        return None

    async def add_birthday(
        self, chat_id: int, owner: str, event_date: datetime.date
    ) -> Event:
        event = Event(
            chat_id=chat_id,
            event_type=EventType.BIRTHDAY,
            owner=owner,
            event_date=event_date,
        )
        await self.event_repository.add(event)

        return event

    async def update_birthday(
        self, chat_id: int, owner: str, event_date: datetime.date
    ) -> Event:
        event = await self.event_repository.update(
            chat_id=chat_id, owner=owner, event_date=event_date
        )

        return event

    async def delete_birthday(
        self,
        chat_id: int,
        owner: str,
        event_type: EventType = EventType.BIRTHDAY,
    ) -> None:
        await self.event_repository.delete(
            chat_id=chat_id, owner=owner, event_type=event_type
        )

    async def get_birthdays(self, chat_id: int) -> list[Event]:
        return await self.event_repository.get_by_chat_id(
            chat_id=chat_id,
            event_type=EventType.BIRTHDAY,
        )
