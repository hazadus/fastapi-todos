import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.constants import AUTH_ALGORITHM
from app.db import UserDAO, get_session
from app.models import UserModel

auth_header = HTTPBearer()


async def get_current_user(
    *,
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(auth_header),
) -> UserModel:
    """
    Возвращает текущего пользователя, при наличии верного токена в заголовке
    запроса. В случае проблем с аутентификацией, вызывает `HTTPException` со
    статус-кодом 401.
    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
        credentials (HTTPAuthorizationCredentials): Данные аутентификации из
            заголовка запроса, содержащие токен.
    Returns:
        UserModel: Модель пользователя, если токен действителен.
    Raises:
        HTTPException: Если токен недействителен или пользователь не найден.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ошибка валидации токена аутентификации",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials.scheme == "Bearer":
        raise credentials_exception
    token: str = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[AUTH_ALGORITHM],
        )
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError):
        raise credentials_exception

    current_user = await UserDAO.find_one_or_none(
        session=session,
        email=email,
    )

    # Если пользователь не найден, в целях безопасности не раскрываем,
    # что токен был действителен, просто возвращаем ошибку
    # аутентификации.
    if current_user is None:
        raise credentials_exception

    return current_user
