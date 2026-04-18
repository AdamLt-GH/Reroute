from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.database.session import Database


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # keep one engine for the app instead of rebuilding it per request
        app.state.database = Database(settings.database_url)
        yield
        await app.state.database.close()

    app = FastAPI(
        title="Reroute API",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
