"""Содержит функции для работы с хэшами паролей."""

from passlib.context import CryptContext

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
