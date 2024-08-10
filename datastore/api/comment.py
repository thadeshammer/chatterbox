import logging
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from datastore.entities.models import CommentCreate, CommentRead
from datastore.exceptions import NotFoundError
from datastore.queries import (
    create_comment,
    delete_comment,
    get_comment_by_id,
    get_comments_by_post_id,
    get_comments_by_user_id,
)

comment_routes = APIRouter()

logger = logging.getLogger(__name__)


@comment_routes.get("/", response_model=Union[CommentRead, list[CommentRead]])
async def get_comments_endpoint(
    comment_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    post_id: Optional[str] = Query(None),
) -> Union[CommentRead, list[CommentRead]]:
    try:
        if comment_id:
            comment = await get_comment_by_id(comment_id)
            if comment is None:
                raise HTTPException(status_code=404, detail="Comment not found")
            return comment
        elif user_id:
            comments = await get_comments_by_user_id(user_id)
            if not comments:
                raise HTTPException(status_code=404, detail="Comments not found")
            return comments
        elif post_id:
            comments = await get_comments_by_post_id(post_id)
            if not comments:
                raise HTTPException(status_code=404, detail="Comments not found")
            return comments
        else:
            raise HTTPException(status_code=400, detail="No query parameters provided")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


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


@comment_routes.delete("/", status_code=204)
async def delete_comment_endpoint(comment_id: str = Query(...)):
    try:
        await delete_comment(comment_id)
    except NotFoundError as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e
