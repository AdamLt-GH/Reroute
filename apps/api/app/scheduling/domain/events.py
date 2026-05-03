from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from app.scheduling.domain.time import require_aware


class EventValidationError(ValueError):
    pass


@dataclass(frozen=True)
class FixedEventWindow:
    id: UUID
    title: str
    start: datetime
    end: datetime
    travel_before_minutes: int = 0
    travel_after_minutes: int = 0

    @property
    def blocked_start(self) -> datetime:
        return self.start - timedelta(minutes=self.travel_before_minutes)

    @property
    def blocked_end(self) -> datetime:
        return self.end + timedelta(minutes=self.travel_after_minutes)


def validate_event(event: FixedEventWindow) -> FixedEventWindow:
    require_aware(event.start)
    require_aware(event.end)

    if event.start >= event.end:
        raise EventValidationError("event end must be after its start")
    if event.travel_before_minutes < 0 or event.travel_after_minutes < 0:
        raise EventValidationError("travel time cannot be negative")

    return event


def events_overlap(first: FixedEventWindow, second: FixedEventWindow) -> bool:
    validate_event(first)
    validate_event(second)
    return first.blocked_start < second.blocked_end and (
        second.blocked_start < first.blocked_end
    )


def find_event_conflicts(
    events: list[FixedEventWindow],
) -> list[tuple[UUID, UUID]]:
    conflicts: list[tuple[UUID, UUID]] = []

    for index, first in enumerate(events):
        for second in events[index + 1 :]:
            if events_overlap(first, second):
                conflicts.append((first.id, second.id))

    return conflicts
