import asyncio
import datetime
import logging
from collections import defaultdict

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.domain.enums import EventType
from app.infrastructure.db.mappers.events import EventOrm
from app.infrastructure.db.repository import EventRepository

# from app.presentation.bot

log = logging.getLogger(__name__)


class BirthdayScheduler:
    def __init__(
        self,
        event_repository: EventRepository,
        bot: Bot,
    ):
        self.bot = bot
        self.event_repository = event_repository
        self.scheduler = AsyncIOScheduler()

    def __check_good_date(self, event: EventOrm) -> bool:
        today = datetime.date.today()
        check = (
            event.event_type == EventType.BIRTHDAY
            and event.event_date == today
        )
        log.debug("Checking event %s", event)

        return check

    async def check_and_send_messages(self) -> dict[int, list[str]]:
        events = await self.event_repository.list_all()

        all_messages: defaultdict[int, list[str]] = defaultdict(list)

        for event in events:
            if self.__check_good_date(event):
                all_messages[event.chat_id].append(event.owner)

        for chat_id, messages in all_messages.items():
            await self.bot.send_message(chat_id, "\n".join(messages))
        log.info("Today's birthday messages: %s", len(all_messages))

        return all_messages

    async def start(self, notification_time: datetime.time):
        log.info("Starting birthday scheduler")

        self.scheduler.add_job(
            func=lambda: asyncio.create_task(self.check_and_send_messages()),
            trigger='cron',
            hour=notification_time.hour,
            minute=notification_time.minute,
        )

        self.scheduler.start()
