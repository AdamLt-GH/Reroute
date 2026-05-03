from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.repositories.availability import AvailabilityRepository
from app.schemas.availability import AvailabilityCreate
from app.services.availability import (
    AvailabilityNotFoundError,
    AvailabilityService,
)


@pytest.mark.asyncio
async def test_availability_service_creates_an_owned_window() -> None:
    repository = AsyncMock(spec=AvailabilityRepository)
    repository.add.side_effect = lambda window: window
    user_id = uuid4()

    window = await AvailabilityService(repository).create(
        user_id,
        AvailabilityCreate(
            name="Weeknight study",
            day_of_week=1,
            start_time="18:00",
            end_time="21:30",
        ),
    )

    assert window.user_id == user_id
    assert window.name == "Weeknight study"


@pytest.mark.asyncio
async def test_availability_service_hides_other_users_windows() -> None:
    repository = AsyncMock(spec=AvailabilityRepository)
    repository.delete_for_user.return_value = False

    with pytest.raises(AvailabilityNotFoundError):
        await AvailabilityService(repository).delete(uuid4(), uuid4())
