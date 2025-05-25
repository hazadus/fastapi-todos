import jwt

from app.core.config import settings
from app.core.constants import AUTH_ALGORITHM
from app.utils.security import (
    create_access_token,
    hash_password,
    verify_password,
)


def test_hash_password():
    """Тестирует функцию хэширования пароля."""
    password = "my_secure_password"
    hashed_password = hash_password(plaintext=password)

    assert hashed_password is not None
    assert hashed_password != password
    assert verify_password(plain_password=password, hashed=hashed_password)


def test_verify_password():
    """Тестирует функцию проверки пароля."""
    password = "my_secure_password"
    hashed_password = hash_password(plaintext=password)

    assert verify_password(plain_password=password, hashed=hashed_password)
    assert not verify_password(plain_password="wrong_password", hashed=hashed_password)


def test_create_access_token():
    """Тестирует функцию создания токена доступа."""
    email = "user@example.com"
    token = create_access_token(email=email)

    payload = jwt.decode(
        token,
        settings.AUTH_SECRET_KEY,
        algorithms=[AUTH_ALGORITHM],
    )
    token_email: str = payload.get("sub")

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0
    assert token_email == email
