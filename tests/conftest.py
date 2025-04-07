import asyncio
import os
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app
from tests.utils import mock_scalar_result, mock_scalar_result_all

load_dotenv()
TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')


@pytest_asyncio.fixture
async def mock_db_session():
    session = AsyncMock()
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def client(setup_db):
    FastAPICache.init(InMemoryBackend(), prefix="test-cache")
    engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session_test = sessionmaker(
        engine_test, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_db():
        async with async_session_test() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


@pytest.fixture
def mock_execute_result():
    def _mock_execute(return_value):
        return mock_scalar_result(return_value)

    return _mock_execute


@pytest.fixture
def mock_execute_result_all():
    def _mock_execute(return_list):
        return mock_scalar_result_all(return_list)

    return _mock_execute


@pytest.fixture(autouse=True)
def disable_cache():
    FastAPICache.clear()
    yield
    FastAPICache.clear()
