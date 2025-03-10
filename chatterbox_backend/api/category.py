# /chatterbox_backend/api/category.py
# prefix: /category
import logging
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from chatterbox_backend.entities.models import CategoryCreate, CategoryRead
from chatterbox_backend.exceptions import NotFoundError
from chatterbox_backend.queries import (
    create_category,
    delete_category,
    get_categories_by_board_id,
    get_category_by_id,
)

category_routes = APIRouter()

logger = logging.getLogger(__name__)


@category_routes.get("/", response_model=Union[CategoryRead, list[CategoryRead]])
async def get_categories_endpoint(
    category_id: Optional[str] = Query(None),
    board_id: Optional[str] = Query(None),
) -> Union[CategoryRead, list[CategoryRead]]:
    try:
        if category_id:
            return await get_category_by_id(category_id)
        if board_id:
            return await get_categories_by_board_id(board_id)
        return []
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@category_routes.post("/", response_model=CategoryRead)
async def create_category_endpoint(category: CategoryCreate):
    try:
        return await create_category(category)
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@category_routes.delete("/", status_code=204)
async def delete_category_endpoint(category_id: str = Query(...)):
    try:
        await delete_category(category_id)
    except NotFoundError as e:
        logger.info(str(e))
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e
