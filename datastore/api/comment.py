import logging

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from datastore.entities.models import CommentCreate, CommentRead
from datastore.queries import (
    create_comment,
    get_comment_by_id,
    get_comments_by_post_id,
    get_comments_by_user_id,
)

comment_routes = APIRouter()

logger = logging.getLogger(__name__)


@comment_routes.get("/{comment_id}", response_model=CommentRead)
async def get_comment_endpoint(comment_id: str) -> CommentRead:
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


@comment_routes.get("/{comment_id}", response_model=list[CommentRead])
async def get_comments_by_user_id_endpoint(user_id: str) -> list[CommentRead]:
    try:
        comments = await get_comments_by_user_id(user_id)
        if comments is None:
            raise HTTPException(status_code=404, detail="Comment not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return comments


@comment_routes.get("/{comment_id}", response_model=list[CommentRead])
async def get_comments_by_post_id_endpoint(post_id: str) -> list[CommentRead]:
    try:
        comments = await get_comments_by_post_id(post_id)
        if comments is None:
            raise HTTPException(status_code=404, detail="Comment not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return comments


@comment_routes.post("/", response_model=CommentRead)
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
