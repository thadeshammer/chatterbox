import logging
from typing import Optional

from sqlalchemy import not_
from sqlmodel import select

# TODO remove this pylint disable after initial dev push
# pylint: disable=unused-import
from chatterbox_backend.db import async_session
from chatterbox_backend.entities.models import (
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
    Membership,
    MembershipCreate,
    MembershipRead,
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


async def get_user_by_id(
    user_id: str, show_deleted: bool = False
) -> Optional[UserRead]:
    async with async_session() as session:
        query = select(User).where(User.id == user_id)
        if show_deleted is False:
            query = query.where(not_(User.deleted))
        result: UserRead = (await session.execute(query)).unique().scalar_one_or_none()
        response = UserRead.model_validate(result) if result is not None else None
    return response


async def get_user_by_name(
    user_name: str, show_deleted: bool = False
) -> Optional[UserRead]:
    async with async_session() as db:
        query = select(User).where(User.name == user_name)
        if show_deleted is False:
            query = query.where(not_(User.deleted))
        result: User = (await db.execute(query)).unique().scalar_one_or_none()
        response = UserRead.model_validate(result) if result is not None else None
    return response


async def get_board_by_id(
    board_id: str, show_deleted: bool = False
) -> Optional[BoardRead]:
    async with async_session() as session:
        query = select(Board).where(Board.id == board_id)
        if show_deleted is False:
            query = query.where(not_(Board.deleted))
        result: Board = (await session.execute(query)).unique().scalar_one_or_none()
        response = BoardRead.model_validate(result) if result is not None else None
    return response


async def get_all_boards(show_deleted: bool = False) -> list[BoardRead]:
    async with async_session() as session:
        query = select(Board)
        if show_deleted is False:
            query = query.where(not_(Board.deleted))
        results: list[Board] = (await session.execute(query)).unique().scalars().all()
        response = [BoardRead.model_validate(result) for result in results]
    return response


async def get_boards_created_by_user_id(
    user_id: str, show_deleted: bool = False
) -> list[BoardRead]:
    async with async_session() as session:
        query = select(Board).where(Board.user_id == user_id)
        if show_deleted is False:
            query = query.where(not_(Board.deleted))
        results: list[Board] = (await session.execute(query)).unique().scalars().all()
        response = [BoardRead.model_validate(result) for result in results]
    return response


async def get_category_by_id(
    category_id: str, show_deleted: bool = False
) -> Optional[CategoryRead]:
    async with async_session() as session:
        query = select(Category).where(Category.id == category_id)
        if show_deleted is False:
            query = query.where(not_(Category.deleted))
        result: Category = (await session.execute(query)).unique().scalar_one_or_none()
        response = CategoryRead.model_validate(result) if result is not None else None
    return response


async def get_categories_by_board_id(
    board_id: str, show_deleted: bool = False
) -> list[CategoryRead]:
    async with async_session() as session:
        query = select(Category).where(Category.board_id == board_id)
        if show_deleted is False:
            query = query.where(not_(Category.deleted))
        results: list[Category] = (
            (await session.execute(query)).unique().scalars().all()
        )
        response = [CategoryRead.model_validate(result) for result in results]
    return response


async def get_comments_by_post_id(
    post_id: str, show_deleted: bool = False
) -> list[CommentRead]:
    async with async_session() as session:
        if show_deleted is True:
            query = select(Comment).where(Comment.post_id == post_id)
        else:
            query = select(Comment).where(
                Comment.post_id == post_id, not_(Comment.deleted)
            )

        results: list[Comment] = (await session.execute(query)).unique().scalars().all()
        response = [CommentRead.model_validate(result) for result in results]
    return response


async def get_comments_by_user_id(
    user_id: str, show_deleted: bool = False
) -> list[CommentRead]:
    async with async_session() as session:
        if show_deleted is True:
            logger.debug("getting deleted stuff in this get")
            query = select(Comment).where(Comment.user_id == user_id)
        else:
            logger.debug("skipping deleted stuff in this get")
            query = select(Comment).where(
                Comment.user_id == user_id, not_(Comment.deleted)
            )
        results: list[Comment] = (await session.execute(query)).unique().scalars().all()
        logger.debug(f"{len(results)=}")
        response = [CommentRead.model_validate(result) for result in results]
    return response


async def get_comment_by_id(
    comment_id: str, show_deleted: bool = False
) -> Optional[CommentRead]:
    async with async_session() as session:
        query = select(Comment).where(Comment.id == comment_id)
        if show_deleted is False:
            query = query.where(not_(Comment.deleted))
        result: Comment = (await session.execute(query)).unique().scalar_one_or_none()
        response = CommentRead.model_validate(result) if result is not None else None
    return response


async def get_event_by_id(
    event_id: str, show_deleted: bool = False
) -> Optional[EventRead]:
    async with async_session() as session:
        query = select(Event).where(Event.id == event_id)
        if show_deleted is False:
            query = query.where(not_(Event.deleted))
        result: Event = (await session.execute(query)).unique().scalar_one_or_none()
        response = EventRead.model_validate(result) if result is not None else None
    return response


async def get_events_by_board_id(
    board_id: str, show_deleted: bool = False
) -> list[EventRead]:
    async with async_session() as session:
        query = select(Event).where(Event.board_id == board_id)
        if show_deleted is False:
            query = query.where(not_(Event.deleted))
        results: list[Event] = (await session.execute(query)).unique().scalars().all()
        response = [EventRead.model_validate(result) for result in results]
    return response


async def get_post_by_id(
    post_id: str, show_deleted: bool = False
) -> Optional[PostRead]:
    async with async_session() as session:
        query = select(Post).where(Post.id == post_id)
        if show_deleted is False:
            query = query.where(not_(Post.deleted))
        result: Post = (await session.execute(query)).unique().scalar_one_or_none()
        response = PostRead.model_validate(result) if result is not None else None
    return response


async def get_posts_by_category_id(
    category_id: str, show_deleted: bool = False
) -> list[PostRead]:
    async with async_session() as session:
        query = select(Post).where(Post.category_id == category_id)
        if show_deleted is False:
            query = query.where(not_(Post.deleted))
        results: list[Post] = (await session.execute(query)).unique().scalars().all()
        response = [PostRead.model_validate(result) for result in results]
    return response


async def get_user_profile_by_id(
    user_profile_id: str, show_deleted: bool = False
) -> Optional[UserProfileRead]:
    async with async_session() as session:
        query = select(UserProfile).where(UserProfile.id == user_profile_id)
        if show_deleted is False:
            query = query.where(not_(UserProfile.deleted))
        result: UserProfile = (
            (await session.execute(query)).unique().scalar_one_or_none()
        )
        response = (
            UserProfileRead.model_validate(result) if result is not None else None
        )
    return response


async def get_memberships_by_board_id(
    board_id: str, show_deleted: bool = False
) -> list[MembershipRead]:
    async with async_session() as session:
        query = select(Membership).where(Membership.board_id == board_id)
        if show_deleted is False:
            query = query.where(not_(Membership.deleted))
        results: list[Membership] = (
            (await session.execute(query)).unique().scalars().all()
        )
        response = [MembershipRead.model_validate(result) for result in results]
    return response


async def get_memberships_by_user_id(
    user_id: str, show_deleted: bool = False
) -> list[MembershipRead]:
    async with async_session() as session:
        query = select(Membership).where(Membership.user_id == user_id)
        if show_deleted is False:
            query = query.where(not_(Membership.deleted))
        results: list[Membership] = (
            (await session.execute(query)).unique().scalars().all()
        )
        response = [MembershipRead.model_validate(result) for result in results]
    return response
