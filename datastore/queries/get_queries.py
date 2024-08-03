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


async def get_user_by_id(user_id: str) -> Optional[UserRead]:
    async with async_session() as session:
        query = select(User).where(User.id == user_id)
        result: UserRead = (await session.execute(query)).unique().scalar_one_or_none()
        response = UserRead.model_validate(result) if result is not None else None
    return response


async def get_user_by_name(user_name: str) -> Optional[UserRead]:
    async with async_session() as db:
        query = select(User).where(User.name == user_name)
        result: User = (await db.execute(query)).unique().scalar_one_or_none()
        response = UserRead.model_validate(result) if result is not None else None
    return response


async def get_board_by_id(board_id: str) -> Optional[BoardRead]:
    async with async_session() as session:
        query = select(Board).where(Board.id == board_id)
        result: Board = (await session.execute(query)).unique().scalar_one_or_none()
        response = BoardRead.model_validate(result) if result is not None else None
    return response


async def get_all_boards() -> list[BoardRead]:
    async with async_session() as session:
        query = select(Board)
        results: list[Board] = (await session.execute(query)).unique().scalars().all()
        response = [BoardRead.model_validate(result) for result in results]
    return response


async def get_boards_created_by_user_id(user_id: str) -> list[BoardRead]:
    async with async_session() as session:
        query = select(Board).where(Board.user_id == user_id)
        results: Board = (await session.execute(query)).unique().scalars().all()
        response = [BoardRead.model_validate(result) for result in results]
    return response


async def get_category_by_id(category_id: str) -> Optional[CategoryRead]:
    async with async_session() as session:
        query = select(Category).where(Category.id == category_id)
        result: Category = (await session.execute(query)).unique().scalar_one_or_none()
        response = CategoryRead.model_validate(result) if result is not None else None
    return response


async def get_categories_by_board_id(board_id: str) -> list[CategoryRead]:
    async with async_session() as session:
        query = select(Category).where(Category.board_id == board_id)
        results: list[Category] = (
            (await session.execute(query)).unique().scalars().all()
        )
        response = [CategoryRead.model_validate(result) for result in results]
    return response


async def get_comment_by_id(comment_id: str) -> Optional[CommentRead]:
    async with async_session() as session:
        query = select(Comment).where(Comment.id == comment_id)
        result: Comment = (await session.execute(query)).unique().scalar_one_or_none()
        response = CommentRead.model_validate(result) if result is not None else None
    return response


async def get_event_by_id(event_id: str) -> Optional[EventRead]:
    async with async_session() as session:
        query = select(Event).where(Event.id == event_id)
        result: Event = (await session.execute(query)).unique().scalar_one_or_none()
        response = EventRead.model_validate(result) if result is not None else None
    return response


async def get_post_by_id(post_id: str) -> Optional[PostRead]:
    async with async_session() as session:
        query = select(Post).where(Post.id == post_id)
        result: Post = (await session.execute(query)).unique().scalar_one_or_none()
        response = PostRead.model_validate(result) if result is not None else None
    return response


async def get_user_profile_by_id(user_profile_id: str) -> Optional[UserProfileRead]:
    async with async_session() as session:
        query = select(UserProfile).where(UserProfile.id == user_profile_id)
        result: UserProfile = (
            (await session.execute(query)).unique().scalar_one_or_none()
        )
        response = (
            UserProfileRead.model_validate(result) if result is not None else None
        )
    return response
