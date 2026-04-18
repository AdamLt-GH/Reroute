from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_session
from app.main import app, create_app


def test_health_endpoint_reports_ok() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_checks_the_database() -> None:
    test_app = create_app()
    session = AsyncMock(spec=AsyncSession)

    async def override_session() -> AsyncIterator[AsyncSession]:
        yield session

    test_app.dependency_overrides[get_session] = override_session

    with TestClient(test_app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
    session.execute.assert_awaited_once()


def test_readiness_reports_a_database_failure() -> None:
    test_app = create_app()
    session = AsyncMock(spec=AsyncSession)
    session.execute.side_effect = OperationalError("select 1", {}, Exception())

    async def override_session() -> AsyncIterator[AsyncSession]:
        yield session

    test_app.dependency_overrides[get_session] = override_session

    with TestClient(test_app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {"detail": "database is not ready"}
