"""Модуль содержит обработчики маршрутов для аутентификации и регистрации пользователей."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import SignupRequestSchema, SignupResponseSchema
from app.services import EmailAlreadyExistsException, create_user

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и регистрация"],
)


# MARK: POST
@router.post(
    "/signup",
    summary="Зарегистрировать нового пользователя",
    status_code=status.HTTP_201_CREATED,
)
async def user_signup_route(
    user_data: SignupRequestSchema,
    session: AsyncSession = Depends(get_session),
) -> SignupResponseSchema:
    """
    Регистрация нового пользователя.

    Args:
        user_data: Данные для создания пользователя
        session: Сессия базы данных

    Returns:
        SignupResponseSchema: Данные созданного пользователя

    Raises:
        HTTPException: При попытке создать пользователя с существующим email
    """

    try:
        user = await create_user(
            session=session,
            user_data=user_data,
        )
    except EmailAlreadyExistsException as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ex.msg,
        )

    return SignupResponseSchema(
        user=user,
    )
