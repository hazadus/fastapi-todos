from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreateSchema(BaseModel):
    """Схема для создания пользователя."""

    email: EmailStr = Field(
        description="Email, принадлежащий пользователю.",
    )
    password: str = Field(
        description="Пароль пользователя",
    )


class UserResponseSchema(BaseModel):
    """Схема для ответа с информацией о пользователе."""

    id: int = Field(
        description="Уникальный идентификатор пользователя.",
    )
    email: EmailStr = Field(
        description="Email, принадлежащий пользователю.",
    )
    created_at: datetime = Field(
        description="Дата и время регистрации пользователя",
    )
    updated_at: datetime = Field(
        description="Дата и время изменения информации о пользователе",
    )

    # Для конвертирования моделей SQLAlchemy в Pydantic
    model_config = ConfigDict(from_attributes=True)
