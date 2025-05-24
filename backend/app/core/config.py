from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_VERSION: str = Field("0.0.1")
    PROJECT_NAME: str = Field("Todos Backend")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    LOGFIRE_TOKEN: str | None = Field(None)
    LOGFIRE_SERVICE_NAME: str = Field("Backend")

    class Config:
        case_sensitive = True


settings = Settings()
