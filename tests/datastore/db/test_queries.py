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
    get_board_by_id,
    get_category_by_id,
    get_comment_by_id,
    get_comment_votes,
    get_event_by_id,
    get_event_votes,
    get_post_by_id,
    get_post_votes,
    get_user_profile_by_id,
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


@pytest.mark.asyncio
async def test_get_post_votes(async_session):  # pylint: disable=unused-argument
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
    await create_post_vote(post_vote_create)

    votes: list[PostVoteRead] = await get_post_votes(post_read.id)
    assert len(votes) == 1
    assert votes[0].vote == VoteType.UP


@pytest.mark.asyncio
async def test_get_comment_votes(async_session):  # pylint: disable=unused-argument
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
    await create_comment_vote(comment_vote_create)

    votes: list[CommentVoteRead] = await get_comment_votes(comment_read.id)
    assert len(votes) == 1
    assert votes[0].vote == VoteType.UP


@pytest.mark.asyncio
async def test_get_event_votes(async_session):  # pylint: disable=unused-argument
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
    await create_event_vote(event_vote_create)

    votes: list[EventVoteRead] = await get_event_votes(event_read.id)
    assert len(votes) == 1
    assert votes[0].vote == VoteType.UP


@pytest.mark.asyncio
async def test_get_board_by_id(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)

    fetched_board = await get_board_by_id(board_read.id)
    assert fetched_board is not None
    assert fetched_board.id == board_read.id
    assert fetched_board == board_read


@pytest.mark.asyncio
async def test_get_category_by_id(async_session):  # pylint: disable=unused-argument
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
    fetched_category = await get_category_by_id(category_read.id)
    assert fetched_category is not None
    assert fetched_category.id == category_read.id


@pytest.mark.asyncio
async def test_get_comment_by_id(async_session):  # pylint: disable=unused-argument
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
    fetched_comment = await get_comment_by_id(comment_read.id)
    assert fetched_comment is not None
    assert fetched_comment.id == comment_read.id


@pytest.mark.asyncio
async def test_get_event_by_id(async_session):  # pylint: disable=unused-argument
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
    fetched_event = await get_event_by_id(event_read.id)
    assert fetched_event is not None
    assert fetched_event.id == event_read.id


@pytest.mark.asyncio
async def test_get_post_by_id(async_session):  # pylint: disable=unused-argument
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
    fetched_post = await get_post_by_id(post_read.id)
    assert fetched_post is not None
    assert fetched_post.id == post_read.id


@pytest.mark.asyncio
async def test_get_user_profile_by_id(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    user_profile_create = UserProfileCreate(user_id=user_read.id, birthday=date.today())
    user_profile_read: UserProfileRead = await create_user_profile(user_profile_create)
    fetched_user_profile = await get_user_profile_by_id(user_profile_read.id)
    assert fetched_user_profile is not None
    assert fetched_user_profile.id == user_profile_read.id
