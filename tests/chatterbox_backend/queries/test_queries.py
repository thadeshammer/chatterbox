from datetime import date

import pytest

from chatterbox_backend.entities.models import (
    BoardCreate,
    BoardRead,
    BoardUpdate,
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    CommentCreate,
    CommentRead,
    EventCreate,
    EventRead,
    InviteCreate,
    InviteRead,
    PostCreate,
    PostRead,
    UserCreate,
    UserProfileCreate,
    UserProfileRead,
    UserRead,
    UserUpdate,
)
from chatterbox_backend.queries import (
    create_board,
    create_category,
    create_comment,
    create_event,
    create_invite,
    create_post,
    create_user,
    create_user_profile,
    get_board_by_id,
    get_category_by_id,
    get_comment_by_id,
    get_event_by_id,
    get_post_by_id,
    get_user_profile_by_id,
    update_board,
    update_category,
    update_user,
)


@pytest.mark.asyncio
async def test_create_user(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)
    assert user_read.name == user_create.name


@pytest.mark.asyncio
async def test_create_invite(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read, membership_read = await create_board(board_create)

    assert board_read.user_id == membership_read.user_id

    invite_create = InviteCreate(
        email="someemail@example.com",
        issuing_user_id=user_read.id,
        board_id=board_read.id,
    )
    invite_read: InviteRead = await create_invite(invite_create)

    assert invite_read.email == "someemail@example.com"
    assert invite_read.board_id == board_read.id
    assert invite_read.issuing_user_id == user_read.id


@pytest.mark.asyncio
async def test_update_user(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(
        name="test_name", email="testemail@example.com", nickname="bleepleboi"
    )
    user_read: UserRead = await create_user(user_create)

    assert user_read.name == user_create.name
    assert user_read.nickname == user_create.nickname

    user_update = UserUpdate(nickname="wubwub")
    updated_user = await update_user(user_id=user_read.id, user_update=user_update)

    assert updated_user.nickname == "wubwub"


@pytest.mark.asyncio
async def test_create_user_profile(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    user_profile_create = UserProfileCreate(user_id=user_read.id, birthday=date.today())
    user_profile_read: UserProfileRead = await create_user_profile(user_profile_create)

    assert user_profile_create.birthday == user_profile_read.birthday


@pytest.mark.asyncio
async def test_create_and_update_board(
    async_session,
):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read, _ = await create_board(board_create)
    assert board_read.name == board_create.name

    board_update = BoardUpdate(name="new_name", description="better describing things")
    updated_board = await update_board(board_read.id, board_update)

    assert updated_board.name == "new_name"
    assert updated_board.description == "better describing things"


@pytest.mark.asyncio
async def test_create_and_update_category(
    async_session,
):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read, _ = await create_board(board_create)

    category_create = CategoryCreate(
        name="test category name",
        description="describing things",
        user_id=user_read.id,
        board_id=board_read.id,
    )
    category_read: CategoryRead = await create_category(category_create)
    assert category_read.name == category_create.name

    category_update = CategoryUpdate(name="new category name")
    updated = await update_category(category_read.id, category_update)

    assert updated.name == "new category name"


@pytest.mark.asyncio
async def test_create_event(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read, _ = await create_board(board_create)

    event_create = EventCreate(
        name="test_name",
        content="describing things and things and things",
        event_date=date.today(),
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
    board_read, _ = await create_board(board_create)

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
    board_read, _ = await create_board(board_create)

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
async def test_get_board_by_id(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read, _ = await create_board(board_create)

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
    board_read, _ = await create_board(board_create)

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
    board_read, _ = await create_board(board_create)

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
    board_read, _ = await create_board(board_create)

    event_date = date.today()
    event_create = EventCreate(
        name="test_name",
        content="describing things and things and things",
        event_date=event_date,
        user_id=user_read.id,
        board_id=board_read.id,
    )
    event_read: EventRead = await create_event(event_create)
    fetched_event = await get_event_by_id(event_read.id)
    assert fetched_event is not None
    assert fetched_event.id == event_read.id
    assert fetched_event.event_date == event_date


@pytest.mark.asyncio
async def test_get_post_by_id(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read, _ = await create_board(board_create)

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
