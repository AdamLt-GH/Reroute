from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.repositories.preferences import PreferenceRepository
from app.schemas.preferences import ConstraintCreate, PreferenceCreate
from app.services.preferences import (
    PreferenceItemNotFoundError,
    PreferenceService,
)


@pytest.mark.asyncio
async def test_preference_service_creates_owned_settings() -> None:
    repository = AsyncMock(spec=PreferenceRepository)
    repository.add_constraint.side_effect = lambda constraint: constraint
    repository.add_preference.side_effect = lambda preference: preference
    user_id = uuid4()
    service = PreferenceService(repository)

    constraint = await service.create_constraint(
        user_id,
        ConstraintCreate(
            kind="maximum_daily_work",
            settings={"minutes": 360},
        ),
    )
    preference = await service.create_preference(
        user_id,
        PreferenceCreate(
            kind="schedule_stability",
            weight=2.5,
        ),
    )

    assert constraint.user_id == user_id
    assert constraint.settings == {"minutes": 360}
    assert preference.user_id == user_id
    assert preference.weight == 2.5


@pytest.mark.asyncio
async def test_preference_service_hides_another_users_settings() -> None:
    repository = AsyncMock(spec=PreferenceRepository)
    repository.delete_preference.return_value = False

    with pytest.raises(PreferenceItemNotFoundError):
        await PreferenceService(repository).delete_preference(
            uuid4(),
            uuid4(),
        )
