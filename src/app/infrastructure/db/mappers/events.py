from app.domain.event import Event as EventDomain
from app.infrastructure.db.models.events import Event as EventOrm


def event_to_orm(event: EventDomain) -> EventOrm:
    return EventOrm(
        chat_id=event.chat_id,
        event_type=event.event_type,
        event_date=event.event_date,
        owner=event.owner,
    )


def event_to_domain(event: EventOrm) -> EventDomain:
    return EventDomain(
        chat_id=event.chat_id,
        event_type=event.event_type,
        event_date=event.event_date,
        owner=event.owner,
    )
