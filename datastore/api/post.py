# /datastore/api/post.py
# prefix /post
import logging

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from datastore.entities.models import PostCreate, PostRead
from datastore.queries import create_post, get_post_by_id

post_routes = APIRouter()

logger = logging.getLogger(__name__)


@post_routes.get("/{post_id}", response_model=PostRead)
async def get_post_endpoint(post_id: str) -> PostRead:
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
