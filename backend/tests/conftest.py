import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from app.core.config import settings
from faker import Faker
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

faker = Faker()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        url=str(settings.ASYNC_POSTGRES_URI),
        echo=False,
        future=True,
        poolclass=NullPool,
    )

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        autocommit=False,
    )

    async with engine.connect() as conn:
        tsx = await conn.begin()
        try:
            async with SessionLocal(bind=conn) as session:
                nested_tsx = await conn.begin_nested()
                yield session

                if nested_tsx.is_active:
                    await nested_tsx.rollback()

                await tsx.rollback()
        finally:
            await tsx.close()

        await conn.close()
