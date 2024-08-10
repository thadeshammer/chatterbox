# /chatterbox_backend/api/post.py
# prefix /post
import logging
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from chatterbox_backend.entities.models import PostCreate, PostRead
from chatterbox_backend.exceptions import NotFoundError
from chatterbox_backend.queries import (
    create_post,
    delete_post,
    get_post_by_id,
    get_posts_by_category_id,
)

post_routes = APIRouter()

logger = logging.getLogger(__name__)


@post_routes.get("/", response_model=Union[PostRead, list[PostRead]])
async def get_posts_endpoint(
    post_id: Optional[str] = Query(None),
    category_id: Optional[str] = Query(None),
) -> Union[PostRead, list[PostRead]]:
    try:
        if post_id:
            return await get_post_by_id(post_id)
        if category_id:
            return await get_posts_by_category_id(category_id)
        return []
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@post_routes.post("/", response_model=PostRead)
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


@post_routes.delete("/", status_code=204)
async def delete_post_endpoint(post_id: str = Query(...)):
    try:
        await delete_post(post_id)
    except NotFoundError as e:
        logger.error(str(e))
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e
