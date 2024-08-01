import pytest
from sqlmodel import select

from datastore.entities.models import (
    Board,
    BoardCreate,
    Category,
    CategoryCreate,
    Comment,
    CommentCreate,
    Post,
    PostCreate,
    User,
    UserCreate,
    UserRead,
)

MOCK_CREATE_USER_REQUEST = {"name": "beeeeeghootie", "email": "beeghootie@email.net"}

# NOTE These requests will come with a user id in their payload typically.

# pylint: disable=too-many-locals
MOCK_CREATE_BOARD_REQUEST = {
    "title": "Super Cool Hangout Space",
    "description": "it's in the name, yo",
}

MOCK_CREATE_CATEGORY_REQUEST = {
    "title": "General Chat",
    "description": "a place to talk about cool stuff.",
}

MOCK_CREATE_POST_REQUEST = {
    "title": "today's topic is cats!",
    "content": "You know me, fam, I really just love cats even tho they are dumb.",
}

MOCK_CREATE_COMMENT_REQUEST = {
    "content": "some really insightful stuff saying here i am"
}


@pytest.mark.asyncio
async def test_create_comment(async_session):
    async with async_session.begin():
        create_user = UserCreate(**MOCK_CREATE_USER_REQUEST)
        user_data = User(**create_user.model_dump())
        async_session.add(user_data)
    await async_session.commit()

    async with async_session.begin():
        user_query = select(User).where(User.name == MOCK_CREATE_USER_REQUEST["name"])
        user_read: UserRead = (
            (await async_session.execute(user_query)).unique().scalar_one_or_none()
        )
        user_id: str = user_read.id

    async with async_session.begin():
        make_board_request = MOCK_CREATE_BOARD_REQUEST.copy()
        make_board_request["user_id"] = user_id
        create_board = BoardCreate(**make_board_request)
        board_data = Board(**create_board.model_dump())
        board_id = board_data.id
        async_session.add(board_data)
    await async_session.commit()

    async with async_session.begin():
        make_category_request = MOCK_CREATE_CATEGORY_REQUEST.copy()
        make_category_request["user_id"] = user_id
        make_category_request["board_id"] = board_id
        create_category = CategoryCreate(**make_category_request)
        category_data = Category(**create_category.model_dump())
        category_id = category_data.id
        async_session.add(category_data)
    await async_session.commit()

    async with async_session.begin():
        make_post_request = MOCK_CREATE_POST_REQUEST.copy()
        make_post_request["user_id"] = user_id
        make_post_request["category_id"] = category_id
        create_post = PostCreate(**make_post_request)
        post_data = Post(**create_post.model_dump())
        post_id = post_data.id
        async_session.add(post_data)
    await async_session.commit()

    async with async_session.begin():
        make_comment_request = MOCK_CREATE_COMMENT_REQUEST.copy()
        make_comment_request["user_id"] = user_id
        make_comment_request["post_id"] = post_id
        create_comment = CommentCreate(**make_comment_request)
        comment_data = Comment(**create_comment.model_dump())
        async_session.add(comment_data)
    await async_session.commit()
