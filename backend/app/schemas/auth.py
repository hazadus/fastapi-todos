import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.user import UserResponseSchema


class SignupRequestSchema(BaseModel):
    """Схема для запроса регистрации пользователя."""

    email: EmailStr = Field(
        description="Email, принадлежащий пользователю.",
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description=(
            "Пароль пользователя (минимум 8 символов, "
            "должен содержать буквы, цифры и спецсимволы)"
        ),
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Валидация пароля на соответствие требованиям безопасности."""
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну букву")

        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")

        if not re.search(r"[!@#$%^&*()_+\-=\[\]{}]", v):
            raise ValueError("Пароль должен содержать хотя бы один специальный символ")

        return v


class SignupResponseSchema(BaseModel):
    """Схема для ответа с информацией о зарегистрированном пользователе."""

    user: UserResponseSchema = Field(
        description="Информация о зарегистрированном пользователе.",
    )
    message: str = Field(
        default="Пользователь успешно зарегистрирован.",
        description="Сообщение об успешной регистрации.",
    )


class LoginRequestSchema(BaseModel):
    """Схема для запроса входа пользователя."""

    email: EmailStr = Field(
        description="Email, принадлежащий пользователю.",
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Пароль пользователя.",
    )


class LoginResponseSchema(BaseModel):
    """Схема для ответа с информацией о вошедшем пользователе."""

    user: UserResponseSchema = Field(
        description="Информация о вошедшем пользователе.",
    )
    access_token: str = Field(
        description="JWT токен для доступа к защищённым ресурсам.",
    )
    token_type: str = Field(
        default="Bearer",
        description="Тип токена, обычно 'Bearer'.",
    )
