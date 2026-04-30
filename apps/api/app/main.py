from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.authentication import router as authentication_router
from app.api.routes.users import router as users_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.database.dependencies import get_session
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
    app.include_router(authentication_router)
    app.include_router(users_router)

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready", tags=["system"])
    async def readiness(
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> dict[str, str]:
        try:
            await session.execute(text("select 1"))
        except SQLAlchemyError as error:
            raise HTTPException(
                status_code=503,
                detail="database is not ready",
            ) from error

        return {"status": "ready"}

    return app


app = create_app()
