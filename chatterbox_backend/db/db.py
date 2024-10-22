import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel

from chatterbox_backend.config import Config

logger = logging.getLogger(__name__)
logger.debug(f"DB URI: {Config.get_db_uri()}")

# Creating async engine
async_engine = create_async_engine(
    Config.get_db_uri(), echo=True, future=True, hide_parameters=True
)


@asynccontextmanager
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session


async def async_create_all_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
