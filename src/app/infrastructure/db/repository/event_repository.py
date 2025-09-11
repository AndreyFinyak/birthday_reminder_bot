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


class EventRepository:
    @connection
    async def get_by_owner(
        self, session: AsyncSession, owner: str, event_type: EventType
    ) -> EventDomain | None:
        result = await session.execute(
            select(Event).where(
                Event.owner == owner, Event.event_type == event_type
            )
        )
        event = result.scalar_one_or_none()
        return event_to_domain(event) if event else None

    @connection
    async def add(self, session: AsyncSession, event: EventDomain) -> None:
        existing = await self.get_by_owner(
            session, event.owner, event.event_type
        )
        if existing:
            raise ValueError("Event already exists")

        orm_event = event_to_orm(event)
        session.add(orm_event)
        await session.commit()

    @connection
    async def update(
        self, session: AsyncSession, event: EventDomain, **kwargs
    ) -> None:
        existing = await self.get_by_owner(
            session, event.owner, event.event_type
        )
        if not existing:
            raise ValueError("Event does not exist")

        await session.execute(
            sqlalchemy_update(Event)
            .where(
                Event.owner == event.owner,
                Event.event_type == event.event_type,
            )
            .values(**kwargs)
        )
        await session.commit()

    @connection
    async def delete(self, session: AsyncSession, event: EventDomain) -> None:
        existing = await self.get_by_owner(
            session, event.owner, event.event_type
        )
        if not existing:
            raise ValueError("Event does not exist")

        await session.execute(
            sqlalchemy_delete(Event).where(
                Event.owner == event.owner,
                Event.event_type == event.event_type,
            )
        )
        await session.commit()
