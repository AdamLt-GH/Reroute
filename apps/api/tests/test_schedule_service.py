from datetime import UTC, datetime, time

from app.models.availability import AvailabilityWindow
from app.schemas.schedules import ScheduleRecalculateRequest
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


def test_disruption_request_needs_a_real_time_range() -> None:
    start = datetime(2026, 6, 13, 9, tzinfo=UTC)

    try:
        ScheduleRecalculateRequest(
            title="Unexpected appointment",
            start_at=start,
            end_at=start,
        )
    except ValueError as error:
        assert "after its start" in str(error)
    else:
        raise AssertionError("invalid disruption was accepted")
