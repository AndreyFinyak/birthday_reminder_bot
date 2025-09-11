import asyncio
import logging

from app.config.containers import Container
from app.presentation.handlers.users.birthday import BirthdayHandler

# Логирование
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def main():
    # Создаём контейнер
    container = Container()
    container.init_resources()  # если используются ресурсы
    container.wire(modules=[__name__])

    # Берём объекты из контейнера
    bot = container.bot()
    dp = container.dispatcher()
    event_service = container.event_service()
    container.event_repository()

    # Хендлер
    birthday_handler = BirthdayHandler(event_service)
    birthday_handler.register(dp)

    # Запуск планировщика через сервис
    await event_service.start_scheduler()

    # Запуск polling
    log.info("Bot started")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
