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
    VoteType,
)

from .db import async_session

logger = logging.getLogger(__name__)


# NOTE Yes, I tried generics with this for my first time; it blew up spectacularly. Will play
# more with it later.


async def create_user(user_create: UserCreate) -> UserRead:
    async with async_session() as session:
        user_data = User(**user_create.model_dump())
        session.add(user_data)
        await session.commit()
        await session.refresh(user_data)
        response = UserRead.model_validate(user_data)
    return response


async def create_board(board_create: BoardCreate) -> BoardRead:
    async with async_session() as session:
        board_data = Board(**board_create.model_dump())
        session.add(board_data)
        await session.commit()
        await session.refresh(board_data)
        response = BoardRead.model_validate(board_data)
    return response


async def create_category(category_create: CategoryCreate) -> CategoryRead:
    async with async_session() as session:
        category_data = Category(**category_create.model_dump())
        session.add(category_data)
        await session.commit()
        await session.refresh(category_data)
        response = CategoryRead.model_validate(category_data)
    return response


async def create_comment(comment_create: CommentCreate) -> CommentRead:
    async with async_session() as session:
        comment_data = Comment(**comment_create.model_dump())
        session.add(comment_data)
        await session.commit()
        await session.refresh(comment_data)
        response = CommentRead.model_validate(comment_data)
    return response


async def create_event(event_create: EventCreate) -> EventRead:
    async with async_session() as session:
        event_data = Event(**event_create.model_dump())
        session.add(event_data)
        await session.commit()
        await session.refresh(event_data)
        response = EventRead.model_validate(event_data)
    return response


async def create_post(post_create: PostCreate) -> PostRead:
    async with async_session() as session:
        post_data = Post(**post_create.model_dump())
        session.add(post_data)
        await session.commit()
        await session.refresh(post_data)
        response = PostRead.model_validate(post_data)
    return response


async def create_user_profile(
    user_profile_create: UserProfileCreate,
) -> UserProfileRead:
    async with async_session() as session:
        user_profile_data = UserProfile(**user_profile_create.model_dump())
        session.add(user_profile_data)
        await session.commit()
        await session.refresh(user_profile_data)
        response = UserProfileRead.model_validate(user_profile_data)
    return response


async def create_comment_vote(vote_create: CommentVoteCreate) -> CommentVoteRead:
    async with async_session() as session:
        vote_data = CommentVote(**vote_create.model_dump())
        session.add(vote_data)
        await session.commit()
        await session.refresh(vote_data)
        response = CommentVoteRead.model_validate(vote_data)
    return response


async def create_post_vote(vote_create: PostVoteCreate) -> PostVoteRead:
    async with async_session() as session:
        vote_data = PostVote(**vote_create.model_dump())
        session.add(vote_data)
        await session.commit()
        await session.refresh(vote_data)
        response = PostVoteRead.model_validate(vote_data)
    return response


async def create_event_vote(vote_create: EventVoteCreate) -> EventVoteRead:
    async with async_session() as session:
        vote_data = EventVote(**vote_create.model_dump())
        session.add(vote_data)
        await session.commit()
        await session.refresh(vote_data)
        response = EventVoteRead.model_validate(vote_data)
    return response


async def get_user_by_id(user_id: str) -> Optional[UserRead]:
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.id == user_id)
            result: UserRead = (
                (await session.execute(query)).unique().scalar_one_or_none()
            )
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
        async with session.begin():
            query = select(Board).where(Board.id == board_id)
            result: Board = (await session.execute(query)).unique().scalar_one_or_none()
            response = BoardRead.model_validate(result) if result is not None else None
    return response


async def get_category_by_id(category_id: str) -> Optional[CategoryRead]:
    async with async_session() as session:
        async with session.begin():
            query = select(Category).where(Category.id == category_id)
            result: Category = (
                (await session.execute(query)).unique().scalar_one_or_none()
            )
            response = (
                CategoryRead.model_validate(result) if result is not None else None
            )
    return response


async def get_comment_by_id(comment_id: str) -> Optional[CommentRead]:
    async with async_session() as session:
        async with session.begin():
            query = select(Comment).where(Comment.id == comment_id)
            result: Comment = (
                (await session.execute(query)).unique().scalar_one_or_none()
            )
            response = (
                CommentRead.model_validate(result) if result is not None else None
            )
    return response


async def get_event_by_id(event_id: str) -> Optional[EventRead]:
    async with async_session() as session:
        async with session.begin():
            query = select(Event).where(Event.id == event_id)
            result: Event = (await session.execute(query)).unique().scalar_one_or_none()
            response = EventRead.model_validate(result) if result is not None else None
    return response


async def get_post_by_id(post_id: str) -> Optional[PostRead]:
    async with async_session() as session:
        async with session.begin():
            query = select(Post).where(Post.id == post_id)
            result: Post = (await session.execute(query)).unique().scalar_one_or_none()
            response = PostRead.model_validate(result) if result is not None else None
    return response


async def get_user_profile_by_id(user_profile_id: str) -> Optional[UserProfileRead]:
    async with async_session() as session:
        async with session.begin():
            query = select(UserProfile).where(UserProfile.id == user_profile_id)
            result: UserProfile = (
                (await session.execute(query)).unique().scalar_one_or_none()
            )
            response = (
                UserProfileRead.model_validate(result) if result is not None else None
            )
    return response


async def get_post_votes(post_id: str) -> list[PostVoteRead]:
    async with async_session() as session:
        async with session.begin():
            query = select(PostVote).where(PostVote.post_id == post_id)
            result: list[PostVote] = (await session.execute(query)).scalars().all()
            votes: list[PostVoteRead] = [
                PostVoteRead.model_validate(vote) for vote in result
            ]
    return votes


async def get_comment_votes(comment_id: str) -> list[CommentVoteRead]:
    async with async_session() as session:
        async with session.begin():
            query = select(CommentVote).where(CommentVote.comment_id == comment_id)
            result = (await session.execute(query)).scalars().all()
            votes = [CommentVoteRead.model_validate(vote) for vote in result]
    return votes


async def get_event_votes(event_id: str) -> list[EventVoteRead]:
    async with async_session() as session:
        async with session.begin():
            query = select(EventVote).where(EventVote.event_id == event_id)
            result = (await session.execute(query)).scalars().all()
            votes = [EventVoteRead.model_validate(vote) for vote in result]
    return votes


async def get_post_vote_tallies(post_id: str) -> dict[str, int]:
    async with async_session() as session:
        async with session.begin():
            query = select(PostVote).where(PostVote.post_id == post_id)
            result = (await session.execute(query)).scalars().all()

    total_votes = len(result)
    total_up_votes = sum(1 for vote in result if vote.vote == VoteType.UP)
    total_down_votes = sum(1 for vote in result if vote.vote == VoteType.DOWN)

    return {
        "total_votes": total_votes,
        "total_up_votes": total_up_votes,
        "total_down_votes": total_down_votes,
    }


async def get_comment_vote_tallies(comment_id: str) -> dict[str, int]:
    async with async_session() as session:
        async with session.begin():
            query = select(CommentVote).where(CommentVote.comment_id == comment_id)
            result = (await session.execute(query)).scalars().all()

    total_votes = len(result)
    total_up_votes = sum(1 for vote in result if vote.vote == VoteType.UP)
    total_down_votes = sum(1 for vote in result if vote.vote == VoteType.DOWN)

    return {
        "total_votes": total_votes,
        "total_up_votes": total_up_votes,
        "total_down_votes": total_down_votes,
    }


async def get_event_vote_tallies(event_id: str) -> dict[str, int]:
    async with async_session() as session:
        async with session.begin():
            query = select(EventVote).where(EventVote.event_id == event_id)
            result = (await session.execute(query)).scalars().all()

    total_votes = len(result)
    total_up_votes = sum(1 for vote in result if vote.vote == VoteType.UP)
    total_down_votes = sum(1 for vote in result if vote.vote == VoteType.DOWN)

    return {
        "total_votes": total_votes,
        "total_up_votes": total_up_votes,
        "total_down_votes": total_down_votes,
    }
