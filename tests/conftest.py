from typing import Any, AsyncGenerator, Generator

import beanie
import pytest
from fakeredis import FakeServer
from fakeredis.aioredis import FakeConnection
from fastapi import FastAPI
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import ConnectionPool

from aichat_common.services.redis.dependency import get_redis_pool
from aichat_common.services.bot.dependency import get_bot_service
from aichat_common.settings import settings
from aichat_common.web.application import get_app
from aichat_common.services.bot.service import BotService
from aichat_common.db.dao.bot_dao import BotDAO


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    """
    Fixture to create database connection.

    :yield: nothing.
    """
    client = AsyncIOMotorClient(settings.db_url.human_repr())  # type: ignore
    from aichat_common.db.models import load_all_models

    await beanie.init_beanie(
        database=client[settings.db_base],
        document_models=load_all_models(),  # type: ignore
    )
    yield


@pytest.fixture
async def fake_redis_pool() -> AsyncGenerator[ConnectionPool, None]:
    """
    Get instance of a fake redis.

    :yield: FakeRedis instance.
    """
    server = FakeServer()
    server.connected = True
    pool = ConnectionPool(connection_class=FakeConnection, server=server)

    yield pool

    await pool.disconnect()


@pytest.fixture
async def bot_service(
    fake_redis_pool: ConnectionPool,
) -> BotService:
    """
    Fixture that provides a BotService instance with a fake Redis pool.

    :param fake_redis_pool: The fake Redis connection pool.
    :return: An instance of BotService.
    """
    bot_dao = BotDAO()
    service = BotService(bot_dao=bot_dao, redis_pool=fake_redis_pool)
    return service


@pytest.fixture
def fastapi_app(
    fake_redis_pool: ConnectionPool,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_redis_pool] = lambda: fake_redis_pool
    application.dependency_overrides[get_bot_service] = lambda: BotService(
        BotDAO(), redis_pool=fake_redis_pool
    )
    return application


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test", timeout=2.0) as ac:
        yield ac
