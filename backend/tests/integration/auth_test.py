import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import router as auth_router
from app.models import UserModel
from app.schemas import UserCreateSchema
from app.services import create_user
from tests.integration.conftest import BaseTestRouter


@pytest.fixture()
def user_data() -> UserCreateSchema:
    return UserCreateSchema(
        email="user@example.com",
        password="my_s3cure_p@ssw0rd",
    )


@pytest_asyncio.fixture(scope="function")
async def user(
    session: AsyncSession,
    user_data: UserCreateSchema,
) -> UserModel:
    return await create_user(
        session=session,
        user_data=user_data,
    )


class TestAuthRouter(BaseTestRouter):
    router = auth_router

    async def test_auth_signup(
        self,
        client: AsyncClient,
    ):
        """Тестирует регистрацию пользователя."""
        email = "user@example.com"

        response = await client.post(
            "/auth/signup",
            json={
                "email": email,
                "password": "my_s3cure_p@ssw0rd",
            },
        )
        json = response.json()

        assert response.status_code == 201
        assert json["user"]["email"] == email

    async def test_auth_signup_existing_email(
        self,
        client: AsyncClient,
        user: UserModel,
    ):
        """Тестирует регистрацию пользователя с уже существующим email."""
        # Пользователь в БД уже создан в фикстуре user
        # Пытаемся зарегистрировать его снова
        response = await client.post(
            "/auth/signup",
            json={
                "email": user.email,
                "password": "my_s3cure_p@ssw0rd",
            },
        )

        assert response.status_code == 400

    async def test_auth_login(
        self,
        client: AsyncClient,
        session: AsyncSession,
        user: UserModel,
        user_data: UserCreateSchema,
    ):
        """Тестирует успешный вход пользователя."""
        # Пользователь в БД уже создан в фикстуре user
        # Пытаемся войти
        response = await client.post(
            "/auth/login",
            json={
                "email": user_data.email,
                "password": user_data.password,
            },
        )
        json = response.json()

        assert response.status_code == 200
        assert json["user"]["email"] == user_data.email
        assert "access_token" in json
        assert json["token_type"] == "Bearer"

    async def test_auth_login_with_wrong_password(
        self,
        client: AsyncClient,
        session: AsyncSession,
        user: UserModel,
        user_data: UserCreateSchema,
    ):
        """Тестирует вход существующего пользователя c неверным паролем."""
        # Пользователь в БД уже создан в фикстуре user
        # Пытаемся войти
        response = await client.post(
            "/auth/login",
            json={
                "email": user_data.email,
                "password": "wr0ng_p@ssword",
            },
        )

        assert response.status_code == 401

    async def test_nonexistent_user_login(
        self,
        client: AsyncClient,
    ):
        """Тестирует вход несуществующего пользователя."""
        response = await client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "my_s3cure_p@ssw0rd",
            },
        )

        assert response.status_code == 401

    async def test_auth_me_without_token(
        self,
        client: AsyncClient,
        user: UserModel,
    ):
        """Тестирует получение информации о текущем пользователе без токена."""
        response = await client.get("/auth/me")

        assert response.status_code == 403

    async def test_auth_me_with_token(
        self,
        client: AsyncClient,
        user: UserModel,
    ):
        """Тестирует получение информации о текущем пользователе с токеном."""
        # Сначала логинимся, чтобы получить токен
        login_response = await client.post(
            "/auth/login",
            json={
                "email": user.email,
                "password": "my_s3cure_p@ssw0rd",
            },
        )
        login_json = login_response.json()
        token = login_json["access_token"]

        # Теперь запрашиваем информацию о текущем пользователе
        response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        json = response.json()

        assert response.status_code == 200
        assert json["email"] == user.email
