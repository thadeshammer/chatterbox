from datetime import date

import pytest

from chatterbox_backend.entities.models import (
    BoardCreate,
    BoardRead,
    CategoryCreate,
    CategoryRead,
    CommentCreate,
    CommentRead,
    EventCreate,
    PostCreate,
    PostRead,
    UserCreate,
    UserProfileCreate,
    UserRead,
)
from chatterbox_backend.queries import (
    create_board,
    create_category,
    create_comment,
    create_event,
    create_post,
    create_user,
    create_user_profile,
    delete_board,
    delete_category,
    delete_comment,
    delete_event,
    delete_post,
    delete_user,
    delete_user_profile,
    get_board_by_id,
    get_categories_by_board_id,
    get_category_by_id,
    get_comment_by_id,
    get_comments_by_post_id,
    get_event_by_id,
    get_post_by_id,
    get_posts_by_category_id,
    get_user_by_id,
    get_user_profile_by_id,
)

# pylint: disable=unused-argument


@pytest.mark.asyncio
async def test_delete_board(
    async_session,
):
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

    comment_create1 = CommentCreate(
        content="First comment",
        user_id=user_read.id,
        post_id=post_read.id,
    )
    await create_comment(comment_create1)

    comment_create2 = CommentCreate(
        content="Second comment",
        user_id=user_read.id,
        post_id=post_read.id,
    )
    await create_comment(comment_create2)

    await delete_board(board_read.id)

    deleted_board = await get_board_by_id(board_read.id, show_deleted=True)
    assert deleted_board.deleted is True

    deleted_categories = await get_categories_by_board_id(
        board_read.id, show_deleted=True
    )
    for category in deleted_categories:
        assert category.deleted is True

    deleted_posts = await get_posts_by_category_id(category_read.id, show_deleted=True)
    for post in deleted_posts:
        assert post.deleted is True

    deleted_comments = await get_comments_by_post_id(post_read.id, show_deleted=True)
    for comment in deleted_comments:
        assert comment.deleted is True


@pytest.mark.asyncio
async def test_delete_comment(async_session):
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)

    category_create = CategoryCreate(
        name="test_category",
        description="test description",
        user_id=user_read.id,
        board_id=board_read.id,
    )
    category_read = await create_category(category_create)

    post_create = PostCreate(
        name="test_post",
        content="test content",
        user_id=user_read.id,
        category_id=category_read.id,
    )
    post_read = await create_post(post_create)

    comment_create = CommentCreate(
        content="test comment", user_id=user_read.id, post_id=post_read.id
    )
    comment_read = await create_comment(comment_create)

    await delete_comment(comment_read.id)

    deleted_comment = await get_comment_by_id(comment_read.id, show_deleted=True)
    assert deleted_comment.deleted is True


@pytest.mark.asyncio
async def test_delete_event(async_session):
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
        event_date=date.today(),
        user_id=user_read.id,
        board_id=board_read.id,
    )
    event_read = await create_event(event_create)

    await delete_event(event_read.id)

    deleted_event = await get_event_by_id(event_read.id, show_deleted=True)
    assert deleted_event.deleted is True


@pytest.mark.asyncio
async def test_delete_post(async_session):
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)

    category_create = CategoryCreate(
        name="test_category",
        description="test description",
        user_id=user_read.id,
        board_id=board_read.id,
    )
    category_read = await create_category(category_create)

    post_create = PostCreate(
        name="test_post",
        content="test content",
        user_id=user_read.id,
        category_id=category_read.id,
    )
    post_read = await create_post(post_create)

    comment_create = CommentCreate(
        content="test comment", user_id=user_read.id, post_id=post_read.id
    )
    comment_read = await create_comment(comment_create)

    await delete_post(post_read.id)

    deleted_post = await get_post_by_id(post_read.id, show_deleted=True)
    assert deleted_post.deleted is True

    deleted_comment = await get_comment_by_id(comment_read.id, show_deleted=True)
    assert deleted_comment.deleted is True


@pytest.mark.asyncio
async def test_delete_user(async_session):
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read = await create_user(user_create)

    user_profile_create = UserProfileCreate(user_id=user_read.id, bio="test bio")
    user_profile_read = await create_user_profile(user_profile_create)

    await delete_user(user_read.id)

    deleted_user = await get_user_by_id(user_read.id, show_deleted=True)
    assert deleted_user.deleted is True

    deleted_profile = await get_user_profile_by_id(
        user_profile_read.id, show_deleted=True
    )
    assert deleted_profile.deleted is True


@pytest.mark.asyncio
async def test_delete_user_profile(async_session):
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read = await create_user(user_create)

    user_profile_create = UserProfileCreate(user_id=user_read.id, bio="test bio")
    user_profile_read = await create_user_profile(user_profile_create)

    await delete_user_profile(user_profile_read.id)

    deleted_profile = await get_user_profile_by_id(
        user_profile_read.id, show_deleted=True
    )
    assert deleted_profile.deleted is True


@pytest.mark.asyncio
async def test_delete_category(async_session):
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
        content="First comment",
        user_id=user_read.id,
        post_id=post_read.id,
    )
    comment_read: CommentRead = await create_comment(comment_create)

    await delete_category(category_read.id)

    deleted_category = await get_category_by_id(category_read.id, show_deleted=True)
    assert deleted_category.deleted is True

    deleted_post = await get_post_by_id(post_read.id, show_deleted=True)
    assert deleted_post.deleted is True

    deleted_comment = await get_comment_by_id(comment_read.id, show_deleted=True)
    assert deleted_comment.deleted is True
