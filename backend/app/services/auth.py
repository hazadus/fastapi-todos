"""Содержит функции для аутентификации пользователей."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import UserDAO
from app.models import UserModel
from app.utils.security import create_access_token, verify_password


async def authenticate_user(
    *,
    session: AsyncSession,
    email: str,
    password: str,
) -> UserModel | None:
    """
    Проверяет, существует ли пользователь с указанным email и паролем.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
        email (str): Email пользователя.
        password (str): Пароль пользователя.

    Returns:
        UserModel | None: Пользователь, если найден, иначе None.
    """

    user = await UserDAO.find_one_or_none(
        session=session,
        email=email,
    )

    if user and verify_password(
        plain_password=password,
        hashed=user.password_hash,
    ):
        return user

    return None


def create_user_token(
    *,
    user: UserModel,
) -> str:
    """
    Создаёт токен аутентификации для пользователя.

    Args:
        user (UserModel): Пользователь, для которого создаётся токен.

    Returns:
        str: Закодированный JWT токен.
    """

    return create_access_token(email=user.email)
