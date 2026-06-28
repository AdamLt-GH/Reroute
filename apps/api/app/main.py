from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.authentication import router as authentication_router
from app.api.routes.availability import router as availability_router
from app.api.routes.events import router as events_router
from app.api.routes.preferences import router as preferences_router
from app.api.routes.schedules import router as schedules_router
from app.api.routes.task_dependencies import router as task_dependencies_router
from app.api.routes.tasks import router as tasks_router
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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(authentication_router)
    app.include_router(availability_router)
    app.include_router(events_router)
    app.include_router(preferences_router)
    app.include_router(schedules_router)
    app.include_router(task_dependencies_router)
    app.include_router(tasks_router)
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
