import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from datastore.db.query import (
    create_board,
    create_category,
    create_comment,
    create_event,
    create_post,
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
    get_user_by_id,
    get_user_by_name,
    get_user_profile_by_id,
)
from datastore.entities.models import (
    BoardCreate,
    BoardRead,
    CategoryCreate,
    CategoryRead,
    CommentCreate,
    CommentRead,
    CommentVoteRead,
    EventCreate,
    EventRead,
    EventVoteRead,
    PostCreate,
    PostRead,
    PostVoteRead,
    UserCreate,
    UserProfileCreate,
    UserProfileRead,
    UserRead,
)

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/create/user/", response_model=UserRead)
async def create_user_endpoint(user: UserCreate):
    try:
        user_read: UserRead = await create_user(user)
    except ValidationError as e:
        logger.error(f"Failed to create user: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return user_read


@router.post("/create/board/", response_model=BoardRead)
async def create_board_endpoint(board: BoardCreate):
    try:
        board_read: BoardRead = await create_board(board)
    except ValidationError as e:
        logger.error(f"Failed to create board: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return board_read


@router.get("/get/user/", response_model=UserRead)
async def get_user(
    user_id: Optional[str] = Query(None), user_name: Optional[str] = Query(None)
) -> UserRead:
    try:
        if user_id is not None:
            user = await get_user_by_id(user_id)
        elif user_name is not None:
            user = await get_user_by_name(user_name)
        else:
            raise HTTPException(
                status_code=400, detail="Either user_id or user_name must be provided"
            )

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return user


@router.post("/create/category/", response_model=CategoryRead)
async def create_category_endpoint(category: CategoryCreate):
    try:
        category_read: CategoryRead = await create_category(category)
    except ValidationError as e:
        logger.error(f"Failed to create category: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return category_read


@router.post("/create/comment/", response_model=CommentRead)
async def create_comment_endpoint(comment: CommentCreate):
    try:
        comment_read: CommentRead = await create_comment(comment)
    except ValidationError as e:
        logger.error(f"Failed to create comment: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return comment_read


@router.post("/create/event/", response_model=EventRead)
async def create_event_endpoint(event: EventCreate):
    try:
        event_read: EventRead = await create_event(event)
    except ValidationError as e:
        logger.error(f"Failed to create event: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return event_read


@router.post("/create/post/", response_model=PostRead)
async def create_post_endpoint(post: PostCreate):
    try:
        post_read: PostRead = await create_post(post)
    except ValidationError as e:
        logger.error(f"Failed to create post: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return post_read


@router.post("/create/user_profile/", response_model=UserProfileRead)
async def create_user_profile_endpoint(user_profile: UserProfileCreate):
    try:
        user_profile_read: UserProfileRead = await create_user_profile(user_profile)
    except ValidationError as e:
        logger.error(f"Failed to create user profile: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return user_profile_read


@router.get("/get/board/{board_id}", response_model=BoardRead)
async def get_board(board_id: str) -> BoardRead:
    try:
        board = await get_board_by_id(board_id)
        if board is None:
            raise HTTPException(status_code=404, detail="Board not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return board


@router.get("/get/category/{category_id}", response_model=CategoryRead)
async def get_category(category_id: str) -> CategoryRead:
    try:
        category = await get_category_by_id(category_id)
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return category


@router.get("/get/comment/{comment_id}", response_model=CommentRead)
async def get_comment(comment_id: str) -> CommentRead:
    try:
        comment = await get_comment_by_id(comment_id)
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return comment


@router.get("/get/event/{event_id}", response_model=EventRead)
async def get_event(event_id: str) -> EventRead:
    try:
        event = await get_event_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return event


@router.get("/get/post/{post_id}", response_model=PostRead)
async def get_post(post_id: str) -> PostRead:
    try:
        post = await get_post_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return post


@router.get("/get/user_profile/{user_profile_id}", response_model=UserProfileRead)
async def get_user_profile(user_profile_id: str) -> UserProfileRead:
    try:
        user_profile = await get_user_profile_by_id(user_profile_id)
        if user_profile is None:
            raise HTTPException(status_code=404, detail="User profile not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return user_profile


@router.get("/get/post_votes/{post_id}", response_model=list[PostVoteRead])
async def get_post_votes_endpoint(post_id: str):
    try:
        votes = await get_post_votes(post_id)
        if not votes:
            raise HTTPException(
                status_code=404, detail="Votes not found for the given post ID"
            )
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return votes


@router.get("/get/comment_votes/{comment_id}", response_model=list[CommentVoteRead])
async def get_comment_votes_endpoint(comment_id: str):
    try:
        votes = await get_comment_votes(comment_id)
        if not votes:
            raise HTTPException(
                status_code=404, detail="Votes not found for the given comment ID"
            )
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return votes


@router.get("/get/event_votes/{event_id}", response_model=list[EventVoteRead])
async def get_event_votes_endpoint(event_id: str):
    try:
        votes = await get_event_votes(event_id)
        if not votes:
            raise HTTPException(
                status_code=404, detail="Votes not found for the given event ID"
            )
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return votes
