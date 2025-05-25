import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.main import app as the_app


@pytest_asyncio.fixture(scope="function")
async def client():
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
