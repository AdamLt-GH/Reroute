from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies.users import get_registration_service
from app.main import create_app
from app.models.user import User
from app.services.users import EmailAlreadyRegisteredError, RegistrationService


def registered_user() -> User:
    return User(
        id=uuid4(),
        email="adam@example.com",
        password_hash="not returned",
        display_name="Adam",
        timezone="Australia/Sydney",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )


def test_registration_route_returns_the_safe_user_fields() -> None:
    app = create_app()
    service = AsyncMock(spec=RegistrationService)
    service.register.return_value = registered_user()
    app.dependency_overrides[get_registration_service] = lambda: service

    with TestClient(app) as client:
        response = client.post(
            "/api/users/register",
            json={
                "email": "adam@example.com",
                "password": "a useful password",
                "display_name": "Adam",
            },
        )

    assert response.status_code == 201
    assert response.json()["email"] == "adam@example.com"
    assert "password_hash" not in response.json()


def test_registration_route_reports_an_existing_email() -> None:
    app = create_app()
    service = AsyncMock(spec=RegistrationService)
    service.register.side_effect = EmailAlreadyRegisteredError
    app.dependency_overrides[get_registration_service] = lambda: service

    with TestClient(app) as client:
        response = client.post(
            "/api/users/register",
            json={
                "email": "adam@example.com",
                "password": "a useful password",
                "display_name": "Adam",
            },
        )

    assert response.status_code == 409
