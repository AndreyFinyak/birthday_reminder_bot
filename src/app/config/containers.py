from aiogram import Bot, Dispatcher
from dependency_injector import containers, providers

from app.application.services import EventService, UserService
from app.config.config import settings
from app.infrastructure.db.repository import EventRepository, UserRepository
from app.infrastructure.event_tracker import BirthdayScheduler
from app.presentation.handlers import BaseHandler, BirthdayHandler


class Container(containers.DeclarativeContainer):
    # Tg tools
    bot = providers.Singleton(Bot, token=settings.BOT_TOKEN)
    dispatcher = providers.Singleton(Dispatcher, bot=bot)

    # Репозитории
    event_repository = providers.Singleton(EventRepository)
    user_repository = providers.Singleton(UserRepository)

    # Фоновые задачи
    birthday_scheduler = providers.Singleton(
        BirthdayScheduler,
        bot=bot,
        event_repository=event_repository,
    )

    # Сервисы
    event_service = providers.Singleton(
        EventService,
        event_repository=event_repository,
        birthday_scheduler=birthday_scheduler,
    )

    user_service = providers.Singleton(
        UserService,
        user_repository=user_repository,
    )

    # Хендлеры
    birthday_handler = providers.Singleton(
        BirthdayHandler,
        event_service=event_service,
    )

    base_handler = providers.Singleton(
        BaseHandler,
        user_service=user_service,
    )
