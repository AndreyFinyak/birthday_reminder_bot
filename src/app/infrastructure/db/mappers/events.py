from app.domain.event import Event as EventDomain
from app.infrastructure.db.models.events import Event as EventOrm


def event_to_orm(event: EventDomain) -> EventOrm:
    return EventOrm(
        event_type=event.event_type,
        event_date=event.event_date,
        owner=event.owner,
    )


def event_to_domain(event: EventOrm) -> EventDomain:
    return EventDomain(
        event_type=event.event_type,
        event_date=event.event_date,
        owner=event.owner,
    )
