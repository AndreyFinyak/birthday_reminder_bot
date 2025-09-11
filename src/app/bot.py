import asyncio
import logging
from typing import Annotated

from aiogram import Bot, Dispatcher
from dependency_injector.wiring import Provide, inject

from app.application.services.event_service import EventService
from app.config.config import settings
from app.config.containers import Container
from app.config.logging import configure_logging
from app.presentation.handlers import BaseHandler, BirthdayHandler

configure_logging(settings.LOG_LEVEL)
log = logging.getLogger(__name__)


container = Container()
container.wire(modules=[__name__])


@inject
async def main(
    birthday_handler: Annotated[
        BirthdayHandler, Provide[Container.birthday_handler]
    ],
    base_handler: Annotated[BaseHandler, Provide[Container.base_handler]],
    bot: Annotated[Bot, Provide[Container.bot]],
    dp: Annotated[Dispatcher, Provide[Container.dispatcher]],
    event_service: Annotated[EventService, Provide[Container.event_service]],
):
    # Регестрируем хендлеры
    birthday_handler.register(dp)
    base_handler.register(dp)

    # Запуск планировщика через сервис
    await event_service.start_scheduler(hour=00, minute=1)

    # Запуск polling
    log.info("Bot started")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    # Привязываем контейнер к текущему модулю
    container.wire(modules=[__name__])
    asyncio.run(main())
