from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.preferences import get_preference_service
from app.main import create_app
from app.models.preference import SchedulingConstraint, SchedulingPreference
from app.models.user import User
from app.services.preferences import (
    PreferenceItemNotFoundError,
    PreferenceService,
)


def build_user() -> User:
    return User(
        id=uuid4(),
        email="adam@example.com",
        password_hash="hidden",
        display_name="Adam",
        timezone="Australia/Sydney",
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )


def test_owned_constraints_and_preferences_can_be_created() -> None:
    user = build_user()
    service = AsyncMock(spec=PreferenceService)
    service.create_constraint.side_effect = lambda user_id, request: (
        SchedulingConstraint(
            id=uuid4(),
            user_id=user_id,
            **request.model_dump(),
        )
    )
    service.create_preference.side_effect = lambda user_id, request: (
        SchedulingPreference(
            id=uuid4(),
            user_id=user_id,
            **request.model_dump(),
        )
    )
    app = create_app()
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_preference_service] = lambda: service

    with TestClient(app) as client:
        constraint_response = client.post(
            "/api/scheduling/constraints",
            json={
                "kind": "maximum_daily_work",
                "settings": {"minutes": 360},
            },
        )
        preference_response = client.post(
            "/api/scheduling/preferences",
            json={
                "kind": "schedule_stability",
                "weight": 2.5,
            },
        )

    assert constraint_response.status_code == 201
    assert constraint_response.json()["settings"] == {"minutes": 360}
    assert preference_response.status_code == 201
    assert preference_response.json()["weight"] == 2.5
    service.create_constraint.assert_awaited_once()
    service.create_preference.assert_awaited_once()


def test_missing_owned_preference_returns_not_found() -> None:
    service = AsyncMock(spec=PreferenceService)
    service.delete_preference.side_effect = PreferenceItemNotFoundError
    app = create_app()
    app.dependency_overrides[get_current_user] = build_user
    app.dependency_overrides[get_preference_service] = lambda: service

    with TestClient(app) as client:
        response = client.delete(
            f"/api/scheduling/preferences/{uuid4()}",
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "scheduling preference not found",
    }
