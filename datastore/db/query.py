# datastore/db/query.py
"""Centralized location for app queries to seperate the ORM from the core.
"""
import logging
from typing import Optional

from sqlmodel import select

from datastore.entities.models import (
    Board,
    BoardCreate,
    BoardRead,
    Category,
    CategoryCreate,
    CategoryRead,
    Comment,
    CommentCreate,
    CommentRead,
    CommentVote,
    CommentVoteCreate,
    CommentVoteRead,
    Event,
    EventCreate,
    EventRead,
    EventVote,
    EventVoteCreate,
    EventVoteRead,
    Post,
    PostCreate,
    PostRead,
    PostVote,
    PostVoteCreate,
    PostVoteRead,
    User,
    UserCreate,
    UserProfile,
    UserProfileCreate,
    UserProfileRead,
    UserRead,
)

from .db import async_session

logger = logging.getLogger(__name__)


# NOTE Yes, I tried generics with this for my first time; it blew up spectacularly. Will play
# more with it later.


class DSQueryError(Exception):
    pass


async def create_user(user_create: UserCreate) -> UserRead:
    async with async_session() as session:
        user_data = User(**user_create.model_dump())
        session.add(user_data)
        await session.commit()
        await session.refresh(user_data)
    return UserRead(**user_data.model_dump())


async def create_board(board_create: BoardCreate) -> BoardRead:
    async with async_session() as session:
        board_data = Board(**board_create.model_dump())
        session.add(board_data)
        await session.commit()
        await session.refresh(board_data)
    return BoardRead(**board_data.model_dump())


async def create_category(category_create: CategoryCreate) -> CategoryRead:
    async with async_session() as session:
        category_data = Category(**category_create.model_dump())
        session.add(category_data)
        await session.commit()
        await session.refresh(category_data)
    return CategoryRead(**category_data.model_dump())


async def create_comment(comment_create: CommentCreate) -> CommentRead:
    async with async_session() as session:
        comment_data = Comment(**comment_create.model_dump())
        session.add(comment_data)
        await session.commit()
        await session.refresh(comment_data)
    return CommentRead(**comment_data.model_dump())


async def create_event(event_create: EventCreate) -> EventRead:
    async with async_session() as session:
        event_data = Event(**event_create.model_dump())
        session.add(event_data)
        await session.commit()
        await session.refresh(event_data)
    return EventRead(**event_data.model_dump())


async def create_post(post_create: PostCreate) -> PostRead:
    async with async_session() as session:
        post_data = Post(**post_create.model_dump())
        session.add(post_data)
        await session.commit()
        await session.refresh(post_data)
    return PostRead(**post_data.model_dump())


async def create_user_profile(
    user_profile_create: UserProfileCreate,
) -> UserProfileRead:
    async with async_session() as session:
        user_profile_data = UserProfile(**user_profile_create.model_dump())
        session.add(user_profile_data)
        await session.commit()
        await session.refresh(user_profile_data)
    return UserProfileRead(**user_profile_data.model_dump())


async def create_comment_vote(vote_create: CommentVoteCreate) -> CommentVoteRead:
    async with async_session() as session:
        vote_data = CommentVote(**vote_create.model_dump())
        session.add(vote_data)
        await session.commit()
        await session.refresh(vote_data)
    return CommentVoteRead(**vote_data.model_dump())


async def create_post_vote(vote_create: PostVoteCreate) -> PostVoteRead:
    async with async_session() as session:
        vote_data = PostVote(**vote_create.model_dump())
        session.add(vote_data)
        await session.commit()
        await session.refresh(vote_data)
    return PostVoteRead(**vote_data.model_dump())


async def create_event_vote(vote_create: EventVoteCreate) -> EventVoteRead:
    async with async_session() as session:
        vote_data = EventVote(**vote_create.model_dump())
        session.add(vote_data)
        await session.commit()
        await session.refresh(vote_data)
    return EventVoteRead(**vote_data.model_dump())


async def get_user_by_id(user_id: str) -> Optional[UserRead]:
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.id == user_id)
            result: UserRead = (
                (await session.execute(query)).unique().scalar_one_or_none()
            )
    if result is not None:
        return UserRead(**result.model_dump())

    return None


async def get_user_by_name(user_name: str) -> Optional[UserRead]:
    async with async_session() as db:
        logger.debug(f"selecting for {user_name}")
        query = select(User).where(User.name == user_name)
        logger.debug(f"{query=}")
        result: User = (await db.execute(query)).unique().scalar_one_or_none()
        logger.debug(f"got {result=}")

    if result is not None:
        return UserRead(**result.model_dump())

    return None
