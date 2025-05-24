from typing import Literal

from pydantic import BaseModel, Field


class HealthcheckResponseSchema(BaseModel):
    """Схема ответа эндпоинта проверки доступности сервиса"""

    status: Literal["OK"] = Field(
        description="Статус сервиса.",
    )
    title: str = Field(
        description="Название сервиса.",
        examples=["Todos Backend"],
    )
    version: str = Field(
        description="Версия сервиса.",
        examples=["0.0.1"],
    )
    message: str = Field(
        description="Информационное сообщение.",
        examples=["See /docs for API documentation"],
    )
