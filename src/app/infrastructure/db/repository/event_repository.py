from sqlalchemy.orm import Session

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
    def get_by_owner(
        self, session: Session, owner: str, event_type: EventType
    ) -> EventDomain | None:
        event = (
            session.query(Event)
            .filter_by(owner=owner, event_type=event_type)
            .first()
        )
        return event_to_domain(event) if event else None

    @connection
    def add(self, session: Session, event: EventDomain) -> None:
        event = self.get_by_owner(session, event.owner, event.event_type)
        if event:
            raise ValueError("Event already exists")

        session.add(event_to_orm(event))
        session.commit()

    @connection
    def update(self, session: Session, event: EventDomain) -> None:
        if not self.get_by_owner(session, event.owner, event.event_type):
            raise ValueError("Event does not exist")

        session.merge(event_to_orm(event))
        session.commit()

    @connection
    def delete(self, session: Session, event: EventDomain) -> None:
        if not self.get_by_owner(session, event.owner, event.event_type):
            raise ValueError("Event does not exist")

        session.delete(event_to_orm(event))
        session.commit()
