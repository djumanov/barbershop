from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_name: str = "barbershop"
    debug: bool = False

    # PostgreSQL
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "barbershop"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # JWT
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Cache (configuration only — no cache backend wired up yet)
    cache_enabled: bool = False
    cache_backend: str = "memory"  # "memory" | "redis"
    cache_ttl_seconds: int = 300
    redis_url: str | None = None

    # Background tasks (configuration only — uses FastAPI BackgroundTasks when wired)
    background_tasks_enabled: bool = True
    background_task_timeout_seconds: int = 30

    @property
    def database_url(self) -> str:
        """Async SQLAlchemy URL using the asyncpg driver."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()
