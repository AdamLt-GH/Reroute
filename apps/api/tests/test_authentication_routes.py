from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies.authentication import get_authentication_service
from app.main import create_app
from app.models.user import User
from app.services.authentication import (
    AuthenticationService,
    LoginResult,
)


def build_test_user() -> User:
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


def test_login_sets_an_http_only_session_cookie() -> None:
    app = create_app()
    service = AsyncMock(spec=AuthenticationService)
    service.login.return_value = LoginResult(build_test_user(), "session token")
    app.dependency_overrides[get_authentication_service] = lambda: service

    with TestClient(app) as client:
        response = client.post(
            "/api/auth/login",
            json={
                "email": "adam@example.com",
                "password": "a useful password",
            },
        )

    assert response.status_code == 200
    assert "HttpOnly" in response.headers["set-cookie"]
    assert 'reroute_session="session token"' in response.headers["set-cookie"]


def test_logout_revokes_the_cookie_session() -> None:
    app = create_app()
    service = AsyncMock(spec=AuthenticationService)
    app.dependency_overrides[get_authentication_service] = lambda: service

    with TestClient(app) as client:
        client.cookies.set("reroute_session", "session token")
        response = client.post("/api/auth/logout")

    assert response.status_code == 204
    service.logout.assert_awaited_once_with("session token")
