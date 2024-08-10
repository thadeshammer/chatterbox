import asyncio

import pytest

from datastore.entities.models import (
    BoardCreate,
    BoardRead,
    CategoryCreate,
    CategoryRead,
    CommentCreate,
    CommentRead,
    PostCreate,
    PostRead,
    UserCreate,
    UserRead,
)
from datastore.queries import (
    create_board,
    create_category,
    create_comment,
    create_post,
    create_user,
    get_all_boards,
    get_boards_created_by_user_id,
    get_categories_by_board_id,
    get_comments_by_post_id,
    get_comments_by_user_id,
)

# pylint: disable=unused-argument


async def test_get_categories_by_board_id(async_session):
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)
    assert board_read.name == board_create.name

    tasks = []
    for name in range(3):
        category_create = CategoryCreate(
            name=f"test{name}",
            description=f"describing things {name}",
            user_id=user_read.id,
            board_id=board_read.id,
        )
        tasks.append(create_category(category_create))

    await asyncio.gather(*tasks)

    categories = await get_categories_by_board_id(board_read.id)

    names = [category.name for category in categories]

    assert "test0" in names
    assert "test1" in names
    assert "test2" in names


async def test_get_boards_created_by_user_id(async_session):
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="one",
        description="describing things",
        user_id=user.id,
    )
    board: BoardRead = await create_board(board_create)
    assert board.name == board_create.name

    board_create = BoardCreate(
        name="two",
        description="describing things",
        user_id=user.id,
    )
    board: BoardRead = await create_board(board_create)
    assert board.name == board_create.name

    boards = await get_boards_created_by_user_id(user.id)

    names = [board.name for board in boards]

    assert "one" in names
    assert "two" in names


@pytest.mark.asyncio
async def test_get_comments_by_post_id_and_user_id(
    async_session,
):  # pylint: disable=unused-argument
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
    comment_read1: CommentRead = await create_comment(comment_create1)

    assert comment_read1.deleted is False

    comment_create2 = CommentCreate(
        content="Second comment",
        user_id=user_read.id,
        post_id=post_read.id,
    )
    comment_read2: CommentRead = await create_comment(comment_create2)

    assert comment_read2.deleted is False

    comments = await get_comments_by_post_id(post_read.id)
    assert len(comments) == 2
    contents = [comment.content for comment in comments]
    assert "First comment" in contents
    assert "Second comment" in contents
    # assert comments[0].content == "First comment"
    # assert comments[1].content == "Second comment"

    users_comments = await get_comments_by_user_id(user_read.id)
    assert len(users_comments) == 2
    users_contents = [comment.content for comment in users_comments]
    assert "First comment" in users_contents
    assert "Second comment" in users_contents


async def test_get_all_boards(async_session):
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="one",
        description="describing things",
        user_id=user.id,
    )
    board: BoardRead = await create_board(board_create)
    assert board.name == board_create.name

    board_create = BoardCreate(
        name="two",
        description="describing things",
        user_id=user.id,
    )
    board: BoardRead = await create_board(board_create)
    assert board.name == board_create.name

    boards = await get_all_boards(user.id)

    names = [board.name for board in boards]

    assert "one" in names
    assert "two" in names


async def test_get_all_boards_when_no_boards(async_session):
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user: UserRead = await create_user(user_create)

    boards = await get_all_boards(user.id)
    assert len(boards) == 0
