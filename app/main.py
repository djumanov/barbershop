from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import Settings, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan.

    Startup/shutdown hooks live here. The database engine disposal is
    wired up in Phase 3 (app/core/database.py).
    """
    # Startup
    yield
    # Shutdown


def create_app(config: Settings | None = None) -> FastAPI:
    """Build the FastAPI app, adapting behaviour to the environment.

    Interactive API docs (/docs, /redoc, /openapi.json) are exposed only
    outside production.
    """
    config = config or get_settings()

    docs_url = None if config.is_production else "/docs"
    redoc_url = None if config.is_production else "/redoc"
    openapi_url = None if config.is_production else "/openapi.json"

    app = FastAPI(
        title=config.app_name,
        debug=config.debug,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
        lifespan=lifespan,
    )

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "environment": config.environment}

    return app


app = create_app()
