import logging

from aiogram import Dispatcher, types
from aiogram.filters import Command

from app.application.services.user_service import UserService

log = logging.getLogger(__name__)


class BaseHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def cmd_start(self, message: types.Message) -> None:
        if not message.from_user:
            return

        chat_id = message.chat.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        new_user = await self.user_service.add_user(
            chat_id=chat_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        if not new_user:
            await message.answer(f"🎉 С возвращением, {username}! 🙌😊")
            log.info("User already exists: %s (%s)", username, chat_id)
        else:
            await message.answer(f"👋 Привет, {first_name}! 🎉😊")
            log.info("Add new user: %s (%s)", username, chat_id)

    async def cmd_help(self, message: types.Message) -> None:
        text = (
            "🤖 Я — бот-напоминалка 🎂🎉\n\n"
            "✨ Доступные команды:\n"
            "➡️ /start — приветствие 👋\n"
            "➡️ /help — показать это сообщение 📖\n"
            "➡️ /add_birthday — добавить день рождения 🎂➕\n"
            "➡️ /all_birthdays — показать все дни рождения 📅\n"
            "➡️ /update_birthday — обновить дату дня рождения 🔄🎉\n"
        )
        await message.answer(text)

    def register(self, dp: Dispatcher):
        dp.message.register(self.cmd_start, Command(commands=["start"]))
        dp.message.register(self.cmd_help, Command(commands=["help"]))
