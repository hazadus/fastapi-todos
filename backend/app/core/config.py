from typing import Any

from pydantic import Field, PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_VERSION: str = Field("0.0.1")
    PROJECT_NAME: str = Field("Todos Backend")

    AUTH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(1440)

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    ASYNC_POSTGRES_URI: PostgresDsn | None = None

    LOGFIRE_TOKEN: str | None = Field(None)
    LOGFIRE_SERVICE_NAME: str = Field("Backend")

    class Config:
        case_sensitive = True

    @validator("ASYNC_POSTGRES_URI", pre=True)
    def assemble_async_dsn(
        cls,
        v: str | None,
        values: dict[str, Any],
    ) -> PostgresDsn | str:
        """Собирает DSN для подключения к БД PostgreSQL из настроек окружения."""

        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=int(values.get("POSTGRES_PORT")),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
