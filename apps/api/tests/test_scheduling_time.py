from datetime import UTC, datetime

import pytest

from app.scheduling.domain.time import (
    TimezoneError,
    get_timezone,
    to_local,
    to_utc,
)


def test_sydney_time_converts_to_utc() -> None:
    sydney = get_timezone("Australia/Sydney")
    local_time = datetime(2026, 4, 21, 18, 0, tzinfo=sydney)

    assert to_utc(local_time) == datetime(2026, 4, 21, 8, 0, tzinfo=UTC)


def test_utc_time_converts_back_to_sydney() -> None:
    utc_time = datetime(2026, 4, 21, 8, 0, tzinfo=UTC)

    local_time = to_local(utc_time, "Australia/Sydney")

    assert local_time.hour == 18
    assert str(local_time.tzinfo) == "Australia/Sydney"


def test_naive_times_are_rejected() -> None:
    with pytest.raises(TimezoneError, match="must include a timezone"):
        to_utc(datetime(2026, 4, 21, 18, 0))


def test_unknown_timezones_are_rejected() -> None:
    with pytest.raises(TimezoneError, match="unknown timezone"):
        get_timezone("Somewhere/Imaginary")
