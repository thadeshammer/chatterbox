from datetime import date

import pytest

from chatterbox_backend.entities import EntityPrefix
from chatterbox_backend.entities.models import (
    ActionLog,
    BoardCreate,
    CategoryCreate,
    CategoryRead,
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
)


@pytest.mark.asyncio
async def test_id_correctness(async_session):  # pylint: disable=unused-argument
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    assert EntityPrefix.USER in user_read.id

    user_profile_create = UserProfileCreate(user_id=user_read.id, birthday=date.today())
    user_profile_read: UserProfileRead = await create_user_profile(user_profile_create)

    assert EntityPrefix.USERPROFILE in user_profile_read.id

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read, membership_read = await create_board(board_create)

    assert EntityPrefix.BOARD in board_read.id
    assert EntityPrefix.MEMBERSHIP in membership_read.id

    category_create = CategoryCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
        board_id=board_read.id,
    )
    category_read: CategoryRead = await create_category(category_create)

    assert EntityPrefix.CATEGORY in category_read.id

    event_create = EventCreate(
        name="test_name",
        content="describing things and things and things",
        event_date=date.today(),
        user_id=user_read.id,
        board_id=board_read.id,
    )
    event_read: EventRead = await create_event(event_create)

    assert EntityPrefix.EVENT in event_read.id

    post_create = PostCreate(
        name="test_name",
        content="blerp bleep bloop lorum ipsum whatevs",
        user_id=user_read.id,
        category_id=category_read.id,
    )
    post_read: PostRead = await create_post(post_create)

    assert EntityPrefix.POST in post_read.id

    comment_create = CommentCreate(
        content="describing things",
        user_id=user_read.id,
        post_id=post_read.id,
    )
    comment_read: CommentRead = await create_comment(comment_create)

    assert EntityPrefix.COMMENT in comment_read.id

    invite_create = InviteCreate(
        email="someemail@example.com",
        issuing_user_id=user_read.id,
        board_id=board_read.id,
    )
    invite_read: InviteRead = await create_invite(invite_create)

    assert EntityPrefix.INVITE in invite_read.id

    action_log = ActionLog(endpoint="some_Url", parameters="parameters")
    assert EntityPrefix.ACTION in action_log.id
