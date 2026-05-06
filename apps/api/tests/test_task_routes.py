from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.tasks import get_task_service
from app.main import create_app
from app.models.task import Task
from app.models.user import User
from app.services.tasks import TaskService


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


def build_task(user_id: UUID) -> Task:
    start = datetime(2026, 5, 6, 18, tzinfo=UTC)
    return Task(
        id=uuid4(),
        user_id=user_id,
        title="Finish report",
        description=None,
        estimated_minutes=180,
        remaining_minutes=180,
        actual_minutes=0,
        earliest_start=start,
        deadline=start + timedelta(days=2),
        minimum_session_minutes=30,
        maximum_session_minutes=120,
        preferred_session_minutes=60,
        splittable=True,
        priority="medium",
        difficulty="medium",
        category="Study",
        status="backlog",
    )


def test_owned_tasks_are_listed() -> None:
    user = build_user()
    service = AsyncMock(spec=TaskService)
    service.list.return_value = [build_task(user.id)]
    app = create_app()
    app.dependency_overrides[get_current_user] = lambda: user
    app.dependency_overrides[get_task_service] = lambda: service

    with TestClient(app) as client:
        response = client.get("/api/tasks")

    assert response.status_code == 200
    assert response.json()[0]["title"] == "Finish report"
    service.list.assert_awaited_once_with(user.id)
