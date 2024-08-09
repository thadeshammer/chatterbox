# /datastore/api/category.py
# prefix: /category
import logging

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from datastore.entities.models import CategoryCreate, CategoryRead
from datastore.queries import (
    create_category,
    get_categories_by_board_id,
    get_category_by_id,
)

category_routes = APIRouter()

logger = logging.getLogger(__name__)


@category_routes.get("/board/{board_id}", response_model=list[CategoryRead])
async def get_categories_by_board_id_endpoint(board_id: str) -> list[CategoryRead]:
    try:
        categories = await get_categories_by_board_id(board_id)
        if categories is None:
            raise HTTPException(status_code=404, detail="Category not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return categories


@category_routes.get("/{category_id}", response_model=CategoryRead)
async def get_category_endpoint(category_id: str) -> CategoryRead:
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


@category_routes.post("/", response_model=CategoryRead)
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
