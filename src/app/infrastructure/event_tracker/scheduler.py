import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.domain.enums import EventType
from app.infrastructure.db.mappers.events import EventOrm
from app.infrastructure.db.repository import EventRepository

# from app.presentation.bot


class BirthdayScheduler:
    def __init__(
        self,
        event_repository: EventRepository,
    ):
        self.event_repository = event_repository
        self.scheduler = AsyncIOScheduler()

    def __check_good_date(self, event: EventOrm) -> bool:
        today = datetime.date.today()
        check = (
            event.event_type == EventType.BIRTHDAY
            and event.event_date == today
        )

        return check

    async def check_and_send_messages(self) -> list[str]:
        events = await self.event_repository.list_all()

        all_messages = []
        counter = 0

        for event in events:
            if self.__check_good_date(event):
                all_messages.append(f"{counter}. {event.owner}")
                counter += 1

        return all_messages

    def start(self, notification_time: datetime.time):
        # планируем задачу каждый день в указанное время
        self.scheduler.add_job(
            func=self.check_and_send_messages,
            trigger='cron',
            hour=notification_time.hour,
            minute=notification_time.minute,
        )
        self.scheduler.start()
