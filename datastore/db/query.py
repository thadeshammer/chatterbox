# datastore/db/query.py
"""Centralized location for app queries to seperate the ORM from the core.
"""
import logging
from typing import Optional

from sqlmodel import select

from datastore.entities.models import User, UserCreate, UserRead

from .db import async_session

logger = logging.getLogger(__name__)


class DSQueryError(Exception):
    pass


async def create_user(user_create: UserCreate):
    async with async_session() as session:
        user_data = User(**user_create.model_dump())
        session.add(user_data)
        await session.commit()


async def get_user_by_id(user_id: str) -> Optional[UserRead]:
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.id == user_id)
            result: UserRead = (
                (await session.execute(query)).unique().scalar_one_or_none()
            )
    return result


async def get_user_by_name(user_name: str) -> Optional[UserRead]:
    async with async_session() as db:
        query = select(User).where(User.name == user_name)
        result: UserRead = (await db.execute(query)).unique().scalar_one_or_none()
    return result
