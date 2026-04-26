from datetime import UTC, datetime

import pytest

from app.scheduling.domain.time import (
    TimezoneError,
    get_timezone,
    localise,
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


def test_localise_adds_the_selected_timezone() -> None:
    local_time = localise(
        datetime(2026, 4, 21, 18, 0),
        "Australia/Sydney",
    )

    assert local_time.utcoffset() is not None
    assert str(local_time.tzinfo) == "Australia/Sydney"


def test_localise_rejects_a_time_that_is_already_aware() -> None:
    with pytest.raises(TimezoneError, match="must not already"):
        localise(
            datetime(2026, 4, 21, 18, 0, tzinfo=UTC),
            "Australia/Sydney",
        )


def test_sydney_spring_forward_time_does_not_exist() -> None:
    with pytest.raises(TimezoneError, match="does not exist"):
        localise(
            datetime(2026, 10, 4, 2, 30),
            "Australia/Sydney",
        )
