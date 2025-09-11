import datetime

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
