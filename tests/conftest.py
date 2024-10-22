# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
import asyncio
import logging
from typing import AsyncGenerator

import pytest_asyncio
import redis.asyncio as redis_async
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import text
from sqlmodel import SQLModel

from chatterbox_backend.config import Config
from chatterbox_backend.entities.models import (  # pylint: disable=unused-import
    Board,
    Category,
    Comment,
    Event,
    Membership,
    Post,
    User,
    UserProfile,
)

_TEST_DB_URI = Config.get_db_uri()

logger = logging.getLogger(__name__)
logger.debug(f"{_TEST_DB_URI=}")


@pytest_asyncio.fixture(scope="session")
def event_loop() -> AsyncGenerator[asyncio.AbstractEventLoop, None]:
    """Create and return a new event loop for the session.

    NOTE. This works but it's the old way of doing it and deprecated. I haven't yet figured out how
    to update it. Pytest's docs aren't the best, and my various attempts at making a
    CustomEventLoopPolicy have uniformly failed. For now, this works, let's focus on other things.

    The warning filter in pytest.ini is for this.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop_policy().new_event_loop()

    yield loop

    try:
        loop.close()
    except RuntimeError:
        print("Error trying to close event loop in pytest event_loop fixture.")
        raise


@pytest_asyncio.fixture(scope="session")
async def redis_client(
    event_loop: asyncio.AbstractEventLoop,
) -> AsyncGenerator[redis_async.Redis, None]:
    """Redis client fixture (requires test-redis to be up).

    NOTE. Needed to downgrade from 5.0.7 to 5.0.1 for testing to stop failing/erroring with a
    RunTimeError due to the event loop being closed prior to the redis connection being closed.
        See: https://github.com/redis/redis-py/issues/3239
    Args:
        event_loop (pytest fixture): The test session's custom event loop via fixture.
    """
    redis_instance = redis_async.Redis(**Config.get_redis_args())
    await redis_instance.flushdb()
    yield redis_instance
    await redis_instance.flushdb()
    try:
        await redis_instance.aclose()  # type: ignore
    except RuntimeError:
        print("Error trying to close Redis connection in redis_client fixture.")


@pytest_asyncio.fixture(scope="session")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        _TEST_DB_URI, echo=False, future=True, hide_parameters=False, poolclass=NullPool
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def async_session_maker(
    async_engine: AsyncEngine,
) -> sessionmaker:
    return sessionmaker(async_engine, expire_on_commit=True, class_=AsyncSession)  # type: ignore


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_tables(
    async_engine: AsyncEngine,
) -> AsyncGenerator[None, None]:
    """_summary_

    Args:
        async_engine (pytest fixture): _description_
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def truncate_tables(
    async_engine: AsyncEngine,
) -> AsyncGenerator[None, None]:
    """Clears table data quickly between tests.

    Uses truncate instead of dropping the tables each test.

    Args:
        async_engine (pytest fixture): Instantiates async test db engine.
    """
    async with async_engine.begin() as conn:
        for table in reversed(SQLModel.metadata.sorted_tables):
            await conn.execute(text(f"TRUNCATE TABLE {table.name} CASCADE;"))
        await conn.commit()
    yield


@pytest_asyncio.fixture(scope="function")
async def async_session(
    async_session_maker: sessionmaker, truncate_tables: AsyncGenerator[None, None]
):
    """Yields an async session per function, closing for each post-function teardown."""
    async with async_session_maker() as session:
        yield session
        await session.close()
