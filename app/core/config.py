from functools import lru_cache
from typing import Literal

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
    environment: Literal["development", "production"] = "development"
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

    # Cache — Redis
    cache_enabled: bool = True
    cache_ttl_seconds: int = 300
    redis_url: str = "redis://localhost:6379/0"

    # Message queue — RabbitMQ
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672//"

    # Background tasks — Celery (broker: RabbitMQ, result backend: Redis)
    celery_broker_url: str = "amqp://guest:guest@localhost:5672//"
    celery_result_backend: str = "redis://localhost:6379/1"
    celery_task_timeout_seconds: int = 30

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

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
