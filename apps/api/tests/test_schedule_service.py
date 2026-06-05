from datetime import UTC, datetime, time

from app.models.availability import AvailabilityWindow
from app.services.schedules import expand_availability


def test_weekly_availability_expands_inside_the_horizon() -> None:
    windows = expand_availability(
        [
            AvailabilityWindow(
                name="Monday study",
                day_of_week=0,
                start_time=time(9),
                end_time=time(12),
            )
        ],
        datetime(2026, 6, 1, tzinfo=UTC),
        datetime(2026, 6, 8, tzinfo=UTC),
        "UTC",
    )

    assert len(windows) == 2
    assert windows[0].start.hour == 9
