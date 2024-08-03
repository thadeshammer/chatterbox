# datastore/db/query.py
"""Centralized location for app queries to seperate the ORM from the core.
"""
import logging
from typing import Optional

from sqlmodel import select

# TODO remove this pylint disable after initial dev push
# pylint: disable=unused-import
from datastore.db import async_session
from datastore.entities.models import (
    Board,
    BoardCreate,
    BoardRead,
    BoardUpdate,
    Category,
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    Comment,
    CommentCreate,
    CommentRead,
    Event,
    EventCreate,
    EventRead,
    Post,
    PostCreate,
    PostRead,
    User,
    UserCreate,
    UserProfile,
    UserProfileCreate,
    UserProfileRead,
    UserRead,
    UserUpdate,
)

logger = logging.getLogger(__name__)


async def update_user(user_id: str, user_update: UserUpdate) -> UserRead:
    async with async_session() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user_data = result.scalar_one_or_none()

        if not user_data:
            raise ValueError(f"User with id {user_id} does not exist")

        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user_data, key, value)

        await session.commit()
        await session.refresh(user_data)
        response = UserRead.model_validate(user_data)
    return response


async def update_board(board_id: str, board_update: BoardUpdate) -> BoardRead:
    async with async_session() as session:
        statement = select(Board).where(Board.id == board_id)
        result = await session.execute(statement)
        board_data = result.scalar_one_or_none()

        if not board_data:
            raise ValueError(f"Board with id {board_id} does not exist")

        for key, value in board_update.model_dump(exclude_unset=True).items():
            setattr(board_data, key, value)

        await session.commit()
        await session.refresh(board_data)
        response = BoardRead.model_validate(board_data)
    return response


async def update_category(
    category_id: str, category_update: CategoryUpdate
) -> CategoryRead:
    async with async_session() as session:
        statement = select(Category).where(Category.id == category_id)
        result = await session.execute(statement)
        category_data = result.scalar_one_or_none()

        if not category_data:
            raise ValueError(f"Category with id {category_id} does not exist")

        for key, value in category_update.model_dump(exclude_unset=True).items():
            setattr(category_data, key, value)

        await session.commit()
        await session.refresh(category_data)
        response = CategoryRead.model_validate(category_data)
    return response
