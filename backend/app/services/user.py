"""Сервисные функции для работы с пользователями."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import UserDAO
from app.schemas import UserCreateSchema, UserResponseSchema
from app.services.exceptions import EmailAlreadyExistsException
from app.utils import hash_password


async def create_user(
    *,
    session: AsyncSession,
    user_data: UserCreateSchema,
) -> UserResponseSchema:
    """
    Создаёт нового пользователя.

    Args:
        session (AsyncSession): Сессия базы данных.
        user_data (UserCreateSchema): Данные пользователя для создания.
    Returns:
        UserResponseSchema: Ответ с данными созданного пользователя.
    Raises:
        EmailAlreadyExistsException: Если пользователь с таким email уже существует.
    """

    try:
        db_user = await UserDAO.add(
            session=session,
            obj_in={
                **user_data.model_dump(exclude=("password",)),
                "password_hash": hash_password(plaintext=user_data.password),
            },
        )
    except IntegrityError as ex:
        raise EmailAlreadyExistsException from ex

    return UserResponseSchema.model_validate(db_user)
