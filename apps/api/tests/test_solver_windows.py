from datetime import UTC, datetime
from uuid import uuid4

from app.scheduling.domain.events import FixedEventWindow
from app.scheduling.solver import (
    PlanningInput,
    TimeWindow,
    build_free_windows,
)


def test_fixed_events_are_removed_from_available_time() -> None:
    planning = PlanningInput(
        horizon_start=datetime(2026, 5, 18, 8, tzinfo=UTC),
        horizon_end=datetime(2026, 5, 18, 18, tzinfo=UTC),
        tasks=(),
        fixed_events=(
            FixedEventWindow(
                id=uuid4(),
                title="Class",
                start=datetime(2026, 5, 18, 11, tzinfo=UTC),
                end=datetime(2026, 5, 18, 13, tzinfo=UTC),
                travel_before_minutes=30,
                travel_after_minutes=30,
            ),
        ),
        availability=(
            TimeWindow(
                datetime(2026, 5, 18, 9, tzinfo=UTC),
                datetime(2026, 5, 18, 17, tzinfo=UTC),
            ),
        ),
    )

    free = build_free_windows(planning)

    assert [(window.start.hour, window.end.hour) for window in free] == [
        (9, 10),
        (13, 17),
    ]
    assert free[0].end.minute == 30
    assert free[1].start.minute == 30
