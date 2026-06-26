from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.schedules import get_schedule_service
from app.main import create_app
from app.models.schedule import Schedule, ScheduleBlock
from app.models.user import User
from app.services.schedules import ScheduleService


def user() -> User:
    return User(
        id=uuid4(),
        email="adam@example.com",
        password_hash="hidden",
        display_name="Adam",
        timezone="Australia/Sydney",
        is_active=True,
    )


def schedule(owner_id: UUID, status: str, source: str) -> Schedule:
    start = datetime(2026, 6, 26, 9, tzinfo=UTC)
    return Schedule(
        id=uuid4(),
        user_id=owner_id,
        horizon_start=start,
        horizon_end=datetime(2026, 7, 3, 9, tzinfo=UTC),
        status=status,
        source=source,
        parent_schedule_id=None,
        unscheduled_task_ids=[],
        blocks=[
            ScheduleBlock(
                id=uuid4(),
                task_id=uuid4(),
                title="Finish report",
                start_at=start,
                end_at=datetime(2026, 6, 26, 10, tzinfo=UTC),
                locked=False,
                completed=False,
            )
        ],
    )


def test_generate_accept_and_recalculate_routes_work_together() -> None:
    current_user = user()
    proposed = schedule(current_user.id, "proposed", "initial")
    accepted = schedule(current_user.id, "accepted", "initial")
    revised = schedule(current_user.id, "proposed", "recalculation")
    revised.parent_schedule_id = accepted.id
    service = AsyncMock(spec=ScheduleService)
    service.generate.return_value = proposed
    service.accept.return_value = accepted
    service.recalculate.return_value = revised
    app = create_app()
    app.dependency_overrides[get_current_user] = lambda: current_user
    app.dependency_overrides[get_schedule_service] = lambda: service

    with TestClient(app) as client:
        generated = client.post(
            "/api/schedules/generate",
            json={
                "horizon_start": "2026-06-26T09:00:00Z",
                "horizon_end": "2026-07-03T09:00:00Z",
            },
        )
        accepted_response = client.post(
            f"/api/schedules/{accepted.id}/accept",
        )
        recalculated = client.post(
            f"/api/schedules/{accepted.id}/recalculate",
            json={
                "title": "Unexpected appointment",
                "start_at": "2026-06-27T10:00:00Z",
                "end_at": "2026-06-27T11:00:00Z",
            },
        )

    assert generated.status_code == 201
    assert generated.json()["blocks"][0]["title"] == "Finish report"
    assert accepted_response.json()["status"] == "accepted"
    assert recalculated.status_code == 201
    assert recalculated.json()["source"] == "recalculation"
    service.generate.assert_awaited_once()
    service.accept.assert_awaited_once_with(current_user.id, accepted.id)
    service.recalculate.assert_awaited_once()
