from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies.authentication import get_current_user
from app.api.dependencies.tasks import get_task_dependency_service
from app.main import create_app
from app.models.task import TaskDependency
from app.models.user import User
from app.scheduling.domain.dependencies import DependencyCycleError
from app.services.task_dependencies import TaskDependencyService


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


def build_client(service: AsyncMock) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_current_user] = build_user
    app.dependency_overrides[get_task_dependency_service] = lambda: service
    return TestClient(app)


def test_task_dependency_can_be_created() -> None:
    prerequisite_id = uuid4()
    dependent_id = uuid4()
    service = AsyncMock(spec=TaskDependencyService)
    service.create.return_value = TaskDependency(
        prerequisite_id=prerequisite_id,
        dependent_id=dependent_id,
    )

    with build_client(service) as client:
        response = client.post(
            "/api/task-dependencies",
            json={
                "prerequisite_id": str(prerequisite_id),
                "dependent_id": str(dependent_id),
            },
        )

    assert response.status_code == 201
    assert response.json() == {
        "prerequisite_id": str(prerequisite_id),
        "dependent_id": str(dependent_id),
    }


def test_dependency_cycles_are_explained() -> None:
    first_id = uuid4()
    second_id = uuid4()
    service = AsyncMock(spec=TaskDependencyService)
    service.create.side_effect = DependencyCycleError(
        (first_id, second_id),
    )

    with build_client(service) as client:
        response = client.post(
            "/api/task-dependencies",
            json={
                "prerequisite_id": str(first_id),
                "dependent_id": str(second_id),
            },
        )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "task dependencies contain a cycle",
    }
