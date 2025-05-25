import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.main import app as the_app
from app.models import UserModel
from app.schemas import UserCreateSchema
from app.services import create_user


@pytest_asyncio.fixture(scope="function")
async def client(session: AsyncSession):
    # Подменяем зависимость get_session на нашу тестовую сессию
    the_app.dependency_overrides[get_session] = lambda: session
    transport = ASGITransport(app=the_app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


class BaseTestRouter:
    router = None

    @pytest_asyncio.fixture(scope="function")
    async def client(
        self,
        session: AsyncSession,
    ):
        app = FastAPI()
        app.include_router(self.router)
        # Подменяем зависимость get_session на нашу тестовую сессию
        app.dependency_overrides[get_session] = lambda: session

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c


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
