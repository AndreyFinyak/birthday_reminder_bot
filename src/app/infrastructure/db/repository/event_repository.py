import logging

from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import select
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.enums import EventType
from app.infrastructure.db.database import connection
from app.infrastructure.db.mappers.events import (
    EventDomain,
    event_to_domain,
    event_to_orm,
)
from app.infrastructure.db.models import Event

log = logging.getLogger(__name__)


class EventRepository:
    @connection
    async def get_by_chat_id(
        self, session: AsyncSession, chat_id: int, event_type: EventType
    ) -> EventDomain | None:
        result = await session.execute(
            select(Event).where(
                Event.chat_id == chat_id, Event.event_type == event_type
            )
        )
        event = result.scalar_one_or_none()

        log.debug("Event: %s", event)

        return event_to_domain(event) if event else None

    @connection
    async def add(self, session: AsyncSession, event: EventDomain) -> None:
        existing = await self.get_by_chat_id(
            session, event.chat_id, event.event_type
        )
        if existing:
            raise ValueError("Event already exists")

        orm_event = event_to_orm(event)
        session.add(orm_event)

        log.debug("Event added: %s", orm_event)

        await session.commit()

        return None

    @connection
    async def update(
        self, session: AsyncSession, chat_id: int, owner: str, **kwargs
    ) -> None:
        existing = await self.get_by_chat_id(chat_id=chat_id, owner=owner)
        if not existing:
            raise ValueError("Event does not exist")

        await session.execute(
            sqlalchemy_update(Event)
            .where(Event.chat_id == chat_id, Event.owner == owner)
            .values(**kwargs)
        )
        await session.commit()

        log.warning("Updated: %s", owner)

        return

    @connection
    async def delete(
        self,
        session: AsyncSession,
        chat_id: int,
        owner: str,
        event_type: EventType,
    ) -> None:
        existing = await self.get_by_chat_id(session, chat_id=chat_id)
        if not existing:
            raise ValueError("Event does not exist")

        await session.execute(
            sqlalchemy_delete(Event).where(
                Event.chat_id == chat_id,
                Event.event_type == event_type,
            )
        )
        await session.commit()

        log.warning("Owner deleted: %s", owner)

    @connection
    async def list_all(self, session: AsyncSession) -> list[EventDomain]:
        result = await session.execute(select(Event))
        events = result.scalars().all()
        return [event_to_domain(event) for event in events]
