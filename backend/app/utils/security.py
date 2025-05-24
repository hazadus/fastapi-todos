"""Содержит функции для работы с хэшами паролей."""

from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.constants import AUTH_ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(
    *,
    plain_password: str,
    hashed: str,
) -> bool:
    """
    Проверяет, что plain_password соответствует hashed.

    Args:
        plain_password (str): Обычный пароль, который нужно проверить.
        hashed (str): Хэшированный пароль, с которым нужно сравнить.
    Returns:
        bool: True, если пароли совпадают, иначе False.
    """

    return pwd_context.verify(plain_password, hashed)


def hash_password(
    *,
    plaintext: str,
) -> str:
    """
    Возвращает хэш от строки `plaintext`. Хэши будут каждый раз
    отличаться для одной и той же строки.

    Args:
        plaintext (str): Строка, которую нужно захэшировать.
    Returns:
        str: Хэшированная строка.
    """

    return pwd_context.hash(plaintext)


def create_access_token(
    *,
    email: str,
) -> str:
    """
    Создаёт токен аутентификации (JWT) для пользователя с указанным email.

    Args:
        email (str): Email пользователя, для которого создаётся токен.
    Returns:
        str: Закодированный JWT токен.
    """
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "sub": email,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }

    encoded_jwt = jwt.encode(
        data,
        settings.AUTH_SECRET_KEY,
        algorithm=AUTH_ALGORITHM,
    )

    return encoded_jwt
