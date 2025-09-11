import datetime
import logging

from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError

from app.application.services.event_service import EventService
from app.presentation.handlers.users.states import BirthdayStates
from app.presentation.schemas import BirthdaySchema

log = logging.getLogger(__name__)


class BirthdayHandler:
    def __init__(
        self,
        event_service: EventService,
    ):
        self.event_service = event_service

    async def cmd_add_birthday(
        self, message: types.Message, state: FSMContext
    ) -> None:
        log.debug(
            "chat_id: %s, message_id: %s", message.chat.id, message.message_id
        )
        await message.reply("Введите имя:")
        await state.set_state(BirthdayStates.waiting_for_owner)

        return None

    async def process_owner(
        self, message: types.Message, state: FSMContext
    ) -> None:
        if message.text:
            owner_text = message.text.strip()
        else:
            log.error("invalid owner: %s", message.text)

            await message.reply("Имя не может быть пустым. Повторите ввод:")
            return None

        await state.update_data(owner=owner_text)
        await message.reply("Теперь введите дату в формате ДД-ММ-ГГГГ:")
        await state.set_state(BirthdayStates.waiting_for_date)

        return None

    async def process_date(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        owner = data.get("owner")

        if message.text:
            date_str = message.text.strip()

        # Валидация через Pydantic
        try:
            date = datetime.datetime.strptime(date_str, "%d-%m-%Y").date()

            schema = BirthdaySchema(owner=str(owner), date=date)

        except ValidationError:
            await message.reply(
                "Ошибка!\nПопробуйте ввести дату ещё раз в формате ДД-ММ-ГГГГ."
            )
            return

        # Сохраняем
        await self.event_service.add_birthday(
            chat_id=message.chat.id, owner=schema.owner, event_date=schema.date
        )

        await message.reply(
            f"Событие добавлено: {schema.owner}, {schema.date.isoformat()}"
        )
        await state.clear()

    async def get_all_birthdays(self, message: types.Message):
        chat_id = message.chat.id
        birthdays = await self.event_service.get_all_birthdays(chat_id=chat_id)
        text_output = ""
        for bd in birthdays:
            text_output += f"{bd.owner} - {bd.event_date.isoformat()}\n"

        await message.reply(text_output)

    async def update_birthday(self, message: types.Message, state: FSMContext):
        chat_id = message.chat.id
        birthdays = await self.event_service.get_all_birthdays(chat_id=chat_id)
        if not birthdays:
            await message.reply("У вас нет сохранённых дней рождения.")
            return

        owners = [bd.owner for bd in birthdays]
        owners_list = "\n".join(f"- {o}" for o in owners)
        await message.reply(
            f"Чьи данные хотите обновить?\n{owners_list}\nВведите имя:"
        )
        await state.set_state(BirthdayStates.waiting_for_update_owner)
        return

    async def process_update_owner(
        self, message: types.Message, state: FSMContext
    ):
        if message.text:
            owner_text = message.text.strip()
        else:
            await message.reply("Имя не может быть пустым. Повторите ввод:")
            return

        await state.update_data(update_owner=owner_text)
        await message.reply("Введите новую дату в формате ДД-ММ-ГГГГ:")
        await state.set_state(BirthdayStates.waiting_for_update_date)

        return

    async def process_update_date(
        self, message: types.Message, state: FSMContext
    ):
        data = await state.get_data()
        owner = data.get("update_owner")
        if message.text:
            date_str = message.text.strip()
        else:
            await message.reply("Дата не может быть пустой. Повторите ввод:")
            return
        try:
            date = datetime.datetime.strptime(date_str, "%d-%m-%Y").date()
            schema = BirthdaySchema(owner=str(owner), date=date)
        except ValidationError:
            await message.reply(
                "Ошибка!\nПопробуйте ввести дату ещё раз в формате ДД-ММ-ГГГГ."
            )
            return
        except Exception:
            await message.reply(
                "Ошибка!\nПопробуйте ввести дату ещё раз в формате ДД-ММ-ГГГГ."
            )
            return

        await self.event_service.update_birthday(
            chat_id=message.chat.id, owner=schema.owner, event_date=schema.date
        )
        await message.reply(
            f"День рождения для {schema.owner} "
            f"обновлён на {schema.date.isoformat()}."
        )
        await state.clear()

    def register(self, dp: Dispatcher):
        dp.message.register(
            self.cmd_add_birthday, Command(commands=["add_birthday"])
        )
        dp.message.register(
            self.update_birthday, Command(commands=["update_birthday"])
        )
        dp.message.register(
            self.process_owner, StateFilter(BirthdayStates.waiting_for_owner)
        )
        dp.message.register(
            self.process_date, StateFilter(BirthdayStates.waiting_for_date)
        )
        dp.message.register(
            self.process_update_owner,
            StateFilter(BirthdayStates.waiting_for_update_owner),
        )
        dp.message.register(
            self.process_update_date,
            StateFilter(BirthdayStates.waiting_for_update_date),
        )
        dp.message.register(
            self.get_all_birthdays, Command(commands=["all_birthdays"])
        )
