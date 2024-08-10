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
    Invite,
    InviteCreate,
    InviteRead,
    Membership,
    MembershipCreate,
    MembershipRead,
    Post,
    PostCreate,
    PostRead,
    User,
    UserCreate,
    UserProfile,
    UserProfileCreate,
    UserProfileRead,
    UserRead,
    UserUpdate,
)


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


async def create_invite(invite_create: InviteCreate) -> InviteRead:
    async with async_session() as session:
        invite_data = Invite(**invite_create.model_dump())
        session.add(invite_data)
        await session.commit()
        await session.refresh(invite_data)
        response = InviteRead.model_validate(invite_data)
    return response


async def create_membership(membership_create: MembershipCreate) -> MembershipRead:
    async with async_session() as session:
        membership_data = Membership(**membership_create.model_dump())
        session.add(membership_data)
        await session.commit()
        await session.refresh(membership_data)
        response = MembershipRead.model_validate(membership_data)
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
