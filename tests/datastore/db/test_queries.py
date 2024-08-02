from datetime import date

import pytest

from datastore.db.query import (
    create_board,
    create_category,
    create_comment,
    create_comment_vote,
    create_event,
    create_event_vote,
    create_post,
    create_post_vote,
    create_user,
    create_user_profile,
)
from datastore.entities.models import (
    BoardCreate,
    BoardRead,
    CategoryCreate,
    CategoryRead,
    CommentCreate,
    CommentRead,
    CommentVoteCreate,
    CommentVoteRead,
    EventCreate,
    EventRead,
    EventVoteCreate,
    EventVoteRead,
    PostCreate,
    PostRead,
    PostVoteCreate,
    PostVoteRead,
    UserCreate,
    UserProfileCreate,
    UserProfileRead,
    UserRead,
    VoteType,
)


@pytest.mark.asyncio
async def test_create_user(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)
    assert user_read.name == user_create.name


@pytest.mark.asyncio
async def test_create_user_profile(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    user_profile_create = UserProfileCreate(user_id=user_read.id, birthday=date.today())
    user_profile_read: UserProfileRead = await create_user_profile(user_profile_create)

    assert user_profile_create.birthday == user_profile_read.birthday


@pytest.mark.asyncio
async def test_create_board(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)
    assert board_read.name == board_create.name


@pytest.mark.asyncio
async def test_create_category(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)

    category_create = CategoryCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
        board_id=board_read.id,
    )
    category_read: CategoryRead = await create_category(category_create)
    assert category_read.name == category_create.name


@pytest.mark.asyncio
async def test_create_event(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)

    event_create = EventCreate(
        name="test_name",
        content="describing things and things and things",
        user_id=user_read.id,
        board_id=board_read.id,
    )
    event_read: EventRead = await create_event(event_create)
    assert event_read.name == event_create.name


@pytest.mark.asyncio
async def test_create_post(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)

    category_create = CategoryCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
        board_id=board_read.id,
    )
    category_read: CategoryRead = await create_category(category_create)

    post_create = PostCreate(
        name="test_name",
        content="blerp bleep bloop lorum ipsum whatevs",
        user_id=user_read.id,
        category_id=category_read.id,
    )
    post_read: PostRead = await create_post(post_create)
    assert post_read.name == post_create.name


@pytest.mark.asyncio
async def test_create_comment(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)

    category_create = CategoryCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
        board_id=board_read.id,
    )
    category_read: CategoryRead = await create_category(category_create)

    post_create = PostCreate(
        name="test_name",
        content="blerp bleep bloop lorum ipsum whatevs",
        user_id=user_read.id,
        category_id=category_read.id,
    )
    post_read: PostRead = await create_post(post_create)

    comment_create = CommentCreate(
        content="describing things",
        user_id=user_read.id,
        post_id=post_read.id,
    )
    comment_read: CommentRead = await create_comment(comment_create)
    assert comment_read.content == comment_create.content


@pytest.mark.asyncio
async def test_create_comment_vote(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)

    category_create = CategoryCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
        board_id=board_read.id,
    )
    category_read: CategoryRead = await create_category(category_create)

    post_create = PostCreate(
        name="test_name",
        content="blerp bleep bloop lorum ipsum whatevs",
        user_id=user_read.id,
        category_id=category_read.id,
    )
    post_read: PostRead = await create_post(post_create)

    comment_create = CommentCreate(
        content="describing things",
        user_id=user_read.id,
        post_id=post_read.id,
    )
    comment_read: CommentRead = await create_comment(comment_create)

    comment_vote_create = CommentVoteCreate(
        comment_id=comment_read.id, user_id=user_read.id, vote=VoteType.UP
    )
    comment_vote_read: CommentVoteRead = await create_comment_vote(comment_vote_create)

    assert comment_vote_read.vote == VoteType.UP


@pytest.mark.asyncio
async def test_create_post_vote(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)

    category_create = CategoryCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
        board_id=board_read.id,
    )
    category_read: CategoryRead = await create_category(category_create)

    post_create = PostCreate(
        name="test_name",
        content="blerp bleep bloop lorum ipsum whatevs",
        user_id=user_read.id,
        category_id=category_read.id,
    )
    post_read: PostRead = await create_post(post_create)

    post_vote_create = PostVoteCreate(
        post_id=post_read.id, user_id=user_read.id, vote=VoteType.UP
    )
    post_vote_read: PostVoteRead = await create_post_vote(post_vote_create)

    assert post_vote_read.vote == VoteType.UP


@pytest.mark.asyncio
async def test_create_event_vote(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)

    event_create = EventCreate(
        name="test_name",
        content="describing things and things and things",
        user_id=user_read.id,
        board_id=board_read.id,
    )
    event_read: EventRead = await create_event(event_create)

    event_vote_create = EventVoteCreate(
        event_id=event_read.id, user_id=user_read.id, vote=VoteType.UP
    )
    event_vote_read: EventVoteRead = await create_event_vote(event_vote_create)

    assert event_vote_read.vote == VoteType.UP
