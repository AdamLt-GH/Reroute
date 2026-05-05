from datetime import datetime

from dateutil.rrule import rrulestr

from app.scheduling.domain.events import FixedEventWindow
from app.scheduling.domain.time import require_aware


class RecurrenceError(ValueError):
    pass


def expand_recurrence(
    event: FixedEventWindow,
    rule: str,
    *,
    horizon_start: datetime,
    horizon_end: datetime,
    maximum_occurrences: int = 500,
) -> list[FixedEventWindow]:
    require_aware(horizon_start)
    require_aware(horizon_end)

    if horizon_start >= horizon_end:
        raise RecurrenceError("recurrence horizon is reversed")
    if maximum_occurrences < 1:
        raise RecurrenceError("maximum occurrences must be positive")

    try:
        recurrence = rrulestr(rule, dtstart=event.start)
        starts = []
        for start in recurrence.xafter(
            horizon_start,
            count=maximum_occurrences + 1,
            inc=True,
        ):
            if start > horizon_end:
                break
            starts.append(start)
    except (TypeError, ValueError) as error:
        raise RecurrenceError("recurrence rule is invalid") from error

    if len(starts) > maximum_occurrences:
        raise RecurrenceError("recurrence creates too many events")

    duration = event.end - event.start
    return [
        FixedEventWindow(
            id=event.id,
            title=event.title,
            start=start,
            end=start + duration,
            travel_before_minutes=event.travel_before_minutes,
            travel_after_minutes=event.travel_after_minutes,
        )
        for start in starts
    ]
