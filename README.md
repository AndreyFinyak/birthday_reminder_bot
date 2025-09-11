# Birthday Reminder Bot

Асинхронный Telegram-бот для напоминаний о днях рождения.
Реализован на Python с использованием **aiogram**, **SQLAlchemy**, **APScheduler** и **Pydantic**.

---

## Возможности
- `/start` — регистрация пользователя и приветствие
- `/help` — краткая справка
- `/add_birthday` — добавить день рождения (имя → дата в формате `ДД-ММ-ГГГГ`)
- `/all_birthdays` — показать все сохранённые дни рождения
- `/update_birthday` — обновить дату существующего дня рождения
- Ежедневные уведомления через планировщик

---

## Структура проекта

```
src/app/
├── bot.py                # Точка входа: инициализация бота и планировщика
├── config/               # DI-контейнер и логирование
├── presentation/         # Хендлеры и FSM
│   └── handlers/users/   # BirthdayHandler, BaseHandler
├── application/          # Бизнес-логика: EventService, UserService
├── infrastructure/       # Репозитории, модели БД, планировщик
└── schemas.py            # Pydantic-схемы для валидации
alembic/                  # Миграции базы данных
tests/                    # Юнит-тесты
```

---

## Настройка окружения

1. Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

2. Основные переменные для `.env`:
```env
BOT_TOKEN=<токен Telegram-бота>
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
LOG_LEVEL=INFO
SCHEDULER_ENABLED=true
```

---

## Миграции

Применяем миграции Alembic:
```bash
alembic upgrade head
```

Создание новой миграции:
```bash
alembic revision --autogenerate -m "описание изменений"
```

---

## Запуск бота

### Локально через Poetry:
```bash
poetry run python src/app/bot.py
```

### Локально через venv + pip:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/app/bot.py
```

### Docker (опционально)

Пример `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: birthday_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  bot:
    build: .
    restart: always
    env_file:
      - .env
    depends_on:
      - db

volumes:
  postgres_data:
```

---

## Тесты

Запуск тестов:
```bash
pytest
```
Рекомендуется использовать тестовую БД (SQLite in-memory или отдельный контейнер Postgres).

---

## Отладка и типичные проблемы

- Ошибка `"got multiple values for argument 'session'"` → проверьте декораторы в `src/app/infrastructure/db/database.py`
- Проблемы с подключением к БД → проверьте `DATABASE_URL` и доступность Postgres
- Логи → смотрите `src/app/config/logging.py` и stdout контейнера

---

## Вклад и развитие

- Fork и ветка `feature/...`
- Написание тестов
- PR с описанием изменений

---

## Лицензия

MIT (по умолчанию, замените на актуальную при необходимости)
