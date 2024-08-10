# /datastore/queries/delete_queries.py
from datetime import datetime

from sqlmodel import select

from datastore.db import async_session
from datastore.entities.models import (
    Board,
    Category,
    Comment,
    Event,
    Invite,
    Membership,
    Post,
    User,
    UserProfile,
)


async def delete_comment(comment_id: str):
    async with async_session() as session:
        async with session.begin():
            query = select(Comment).where(Comment.id == comment_id)
            result = await session.execute(query)
            comment_data = result.scalar_one_or_none()

            if comment_data is None:
                raise ValueError(f"No such entity: {comment_id}")
            if comment_data.deleted:
                raise ValueError(f"Comment already deleted: {comment_id}")

            deleted_at = datetime.now()

            comment_data.deleted = True
            comment_data.deleted_at = deleted_at

            await session.commit()
        await session.refresh(comment_data)


async def delete_invite(invite_id: str):
    async with async_session() as session:
        async with session.begin():
            query = select(Invite).where(Invite.id == invite_id)
            result = await session.execute(query)
            invite_data = result.scalar_one_or_none()

            if invite_data is None:
                raise ValueError(f"No such entity: {invite_id}")
            if invite_data.deleted:
                raise ValueError(f"Entity already deleted: {invite_id}")

            deleted_at = datetime.now()

            invite_data.deleted = True
            invite_data.deleted_at = deleted_at

            await session.commit()
        await session.refresh(invite_data)


async def delete_event(event_id: str):
    async with async_session() as session:
        async with session.begin():
            query = select(Event).where(Event.id == event_id)
            result = await session.execute(query)
            event_data = result.scalar_one_or_none()

            if event_data is None:
                raise ValueError(f"No such entity: {event_id}")
            if event_data.deleted:
                raise ValueError(f"Entity already deleted: {event_id}")

            deleted_at = datetime.now()

            event_data.deleted = True
            event_data.deleted_at = deleted_at

            await session.commit()
        await session.refresh(event_data)


async def delete_post(post_id: str):
    async with async_session() as session:
        async with session.begin():
            query = select(Post).where(Post.id == post_id)
            result = await session.execute(query)
            post_data = result.scalar_one_or_none()

            if post_data is None:
                raise ValueError(f"No such entity: {post_id}")
            if post_data.deleted:
                raise ValueError(f"Entity is already deleted: {post_id}")

            deleted_at = datetime.now()

            post_data.deleted = True
            post_data.deleted_at = deleted_at

            for comment in post_data.comments:
                comment.deleted = True
                comment.deleted_at = deleted_at

            await session.commit()
        await session.refresh(post_data)


async def delete_user(user_id: str):
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user_data = result.scalar_one_or_none()

            if not user_data:
                raise ValueError(f"No such entity: {user_id}")
            if user_data.deleted:
                raise ValueError(f"Entity is already deleted: {user_id}")

            deleted_at = datetime.now()
            user_data.deleted = True
            user_data.deleted_at = deleted_at

            if user_data.user_profile is not None:
                user_data.user_profile.deleted = True
                user_data.user_profile.deleted_at = deleted_at

            await session.commit()
        await session.refresh(user_data)


async def delete_user_profile(user_profile_id: str):
    async with async_session() as session:
        async with session.begin():
            query = select(UserProfile).where(UserProfile.id == user_profile_id)
            result = await session.execute(query)
            user_profile_data = result.scalar_one_or_none()

            if not user_profile_data:
                raise ValueError(f"No such entity: {user_profile_id}")
            if user_profile_data.deleted:
                raise ValueError(f"Entity is already deleted: {user_profile_id}")

            deleted_at = datetime.now()
            user_profile_data.deleted = True
            user_profile_data.deleted_at = deleted_at

            await session.commit()
        await session.refresh(user_profile_data)


async def delete_membership(membership_id: str):
    async with async_session() as session:
        async with session.begin():
            query = select(Membership).where(Membership.id == membership_id)
            result = await session.execute(query)
            membership_data = result.scalar_one_or_none()

            if not membership_data:
                raise ValueError(f"No such entity: {membership_id}")
            if membership_data.deleted:
                raise ValueError(f"Entity is already deleted: {membership_id}")

            deleted_at = datetime.now()
            membership_data.deleted = True
            membership_data.deleted_at = deleted_at

            await session.commit()
        await session.refresh(membership_data)


async def delete_category(category_id: str):
    async with async_session() as session:
        async with session.begin():
            query = select(Category).where(Category.id == category_id)
            result = await session.execute(query)
            category_data = result.scalar_one_or_none()

            if not category_data:
                raise ValueError(f"No such entity: {category_id}")
            if category_data.deleted:
                raise ValueError(f"Entity is already deleted: {category_id}")

            deleted_at = datetime.now()
            category_data.deleted = True
            category_data.deleted_at = deleted_at

            for post in category_data.posts:
                for comment in post.comments:
                    comment.deleted = True
                    comment.deleted_at = deleted_at
                post.deleted = True
                post.deleted_at = deleted_at

            await session.commit()
        await session.refresh(category_data)


async def delete_board(board_id: str):
    async with async_session() as session:
        async with session.begin():
            query = select(Board).where(Board.id == board_id)
            result = await session.execute(query)
            board_data = result.scalar_one_or_none()

            if not board_data:
                raise ValueError(f"No such entity: {board_id}")
            if board_data.deleted:
                raise ValueError(f"Entity is already deleted: {board_id}")

            deleted_at = datetime.now()
            board_data.deleted = True
            board_data.deleted_at = deleted_at

            for event in board_data.events:
                event.deleted = True
                event.deleted_at = deleted_at

            for category in board_data.categories:

                category.deleted = True
                category.deleted_at = deleted_at

                for post in category.posts:
                    for comment in post.comments:
                        comment.deleted = True
                        comment.deleted_at = deleted_at
                    post.deleted = True
                    post.deleted_at = deleted_at

            await session.commit()
        await session.refresh(board_data)
