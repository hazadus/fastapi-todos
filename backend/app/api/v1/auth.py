"""Содержит обработчики маршрутов для аутентификации и регистрации пользователей."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db import get_session
from app.models import UserModel
from app.schemas import (
    LoginRequestSchema,
    LoginResponseSchema,
    SignupRequestSchema,
    SignupResponseSchema,
    UserResponseSchema,
)
from app.services import (
    EmailAlreadyExistsException,
    authenticate_user,
    create_user,
    create_user_token,
)

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
async def auth_signup_route(
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


@router.post(
    "/login",
    summary="Получить токен аутентификации",
    status_code=status.HTTP_200_OK,
)
async def auth_login_route(
    login_data: LoginRequestSchema,
    session: AsyncSession = Depends(get_session),
) -> LoginResponseSchema:
    """
    Эндпоинт возвращает токен для аутентификации пользователя в сервисе,
    и информацию о залогиненном пользователе.

    Для доступа к эндпоинтам, предназначенным только для аутентифицированных
    пользователей, полученный токен необходимо передавать в заголовке запросов
    следующим образом:

    `Authorization: Bearer token_value`
    """

    db_user = await authenticate_user(
        session=session,
        email=login_data.email,
        password=login_data.password,
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_user_token(user=db_user)
    user = UserResponseSchema.model_validate(db_user)

    return LoginResponseSchema(
        user=user,
        access_token=token,
    )


# MARK: GET
@router.get(
    "/me",
    summary="Получить информацию о текущем пользователе",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def auth_me_route(
    current_user: UserModel = Depends(get_current_user),
) -> UserResponseSchema:
    """
    Эндпоинт возвращает информацию о текущем аутентифицированном пользователе.

    Для доступа к эндпоинту необходимо передать токен аутентификации в заголовке
    запроса.
    """
    return current_user
