from fastapi.testclient import TestClient

from app.database.session import Database
from app.main import create_app


def test_app_creates_one_database_wrapper_for_its_lifetime() -> None:
    app = create_app()

    with TestClient(app):
        assert isinstance(app.state.database, Database)
