import json
import logging

from app.core.config import Settings
from app.core.logging import JsonFormatter


def test_settings_use_local_service_defaults() -> None:
    settings = Settings()

    assert settings.environment == "development"
    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert settings.frontend_url == "http://localhost:5173"


def test_json_formatter_includes_the_main_log_fields() -> None:
    record = logging.LogRecord(
        name="reroute.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="schedule run queued",
        args=(),
        exc_info=None,
    )

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "INFO"
    assert payload["logger"] == "reroute.test"
    assert payload["event"] == "schedule run queued"
    assert "time" in payload
