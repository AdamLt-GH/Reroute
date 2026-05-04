from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.schemas.events import FixedEventCreate


def test_fixed_event_request_accepts_travel_time() -> None:
    request = FixedEventCreate(
        title="Work shift",
        start_at=datetime(2026, 5, 5, 9, tzinfo=UTC),
        end_at=datetime(2026, 5, 5, 17, tzinfo=UTC),
        travel_before_minutes=30,
        travel_after_minutes=45,
    )

    assert request.travel_before_minutes == 30
    assert request.travel_after_minutes == 45


def test_fixed_event_request_rejects_reversed_times() -> None:
    with pytest.raises(ValidationError):
        FixedEventCreate(
            title="Broken event",
            start_at=datetime(2026, 5, 5, 17, tzinfo=UTC),
            end_at=datetime(2026, 5, 5, 9, tzinfo=UTC),
        )
