# chatterbox_backend/db/query.py
"""Centralized location for app queries to seperate the ORM from the core.
"""
import logging

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
    EventUpdate,
    Membership,
    MembershipCreate,
    MembershipRead,
    MembershipUpdate,
    Post,
    PostCreate,
    PostRead,
    User,
    UserCreate,
    UserProfile,
    UserProfileCreate,
    UserProfileRead,
    UserProfileUpdate,
    UserRead,
    UserUpdate,
)

logger = logging.getLogger(__name__)


async def update_user(user_id: str, user_update: UserUpdate) -> UserRead:
    async with async_session() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user_data = result.scalar_one_or_none()

        if not user_data or user_data.deleted:
            raise ValueError(f"No such entity: {user_id}")

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

        if not board_data or board_data.deleted:
            raise ValueError(f"No such entity: {board_id}")

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

        if not category_data or category_data.deleted:
            raise ValueError(f"No such entity: {category_id}")

        for key, value in category_update.model_dump(exclude_unset=True).items():
            setattr(category_data, key, value)

        await session.commit()
        await session.refresh(category_data)
        response = CategoryRead.model_validate(category_data)
    return response


async def update_membership(
    membership_id: str, membership_update: MembershipUpdate
) -> MembershipRead:
    async with async_session() as session:
        query = select(Membership).where(Membership.id == membership_id)
        result = await session.execute(query)
        membership_data = result.scalar_one_or_none()

        if not membership_data or membership_data.deleted:
            raise ValueError(f"No such entity: {membership_id}")

        for key, value in membership_update.model_dump(exclude_unset=True).items():
            setattr(membership_data, key, value)

        await session.commit()
        await session.refresh(membership_data)
        response = MembershipRead.model_validate(membership_data)
    return response


async def update_user_profile(
    user_profile_id: str, user_profile_update: UserProfileUpdate
) -> UserProfileRead:
    async with async_session() as session:
        query = select(UserProfile).where(UserProfile.id == user_profile_id)
        result = await session.execute(query)
        user_profile_data = result.scalar_one_or_none()

        if not user_profile_data or user_profile_data.deleted:
            raise ValueError(f"No such entity: {user_profile_id}")

        for key, value in user_profile_update.model_dump(exclude_unset=True).items():
            setattr(user_profile_data, key, value)

        await session.commit()
        await session.refresh(user_profile_data)
        response = UserProfileRead.model_validate(user_profile_data)
    return response


# async def update_post(post_id: str, post_update: PostUpdate) -> PostRead:
#     async with async_session() as session:
#         query = select(Post).where(Post.id == post_id)
#         result = await session.execute(query)
#         post_data = result.scalar_one_or_none()

#         if not post_data:
#             raise ValueError(f"Post with id {post_id} does not exist")

#         for key, value in post_update.model_dump(exclude_unset=True).items():
#             setattr(post_data, key, value)

#         await session.commit()
#         await session.refresh(post_data)
#         response = PostRead.model_validate(post_data)
#     return response


async def update_event(event_id: str, event_update: EventUpdate) -> EventRead:
    async with async_session() as session:
        query = select(Event).where(Event.id == event_id)
        result = await session.execute(query)
        event_data = result.scalar_one_or_none()

        if not event_data or event_data.deleted:
            raise ValueError(f"No such entity: {event_id}")

        for key, value in event_update.model_dump(exclude_unset=True).items():
            setattr(event_data, key, value)

        await session.commit()
        await session.refresh(event_data)
        response = EventRead.model_validate(event_data)
    return response


# async def update_comment(comment_id: str, comment_update: CommentUpdate) -> CommentRead:
#     async with async_session() as session:
#         query = select(Comment).where(Comment.id == comment_id)
#         result = await session.execute(query)
#         comment_data = result.scalar_one_or_none()

#         if not comment_data:
#             raise ValueError(f"Comment with id {comment_id} does not exist")

#         for key, value in comment_update.model_dump(exclude_unset=True).items():
#             setattr(comment_data, key, value)

#         await session.commit()
#         await session.refresh(comment_data)
#         response = CommentRead.model_validate(comment_data)
#     return response
