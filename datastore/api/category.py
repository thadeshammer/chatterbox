# /datastore/api/category.py
# prefix: /category
import logging
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from datastore.entities.models import CategoryCreate, CategoryRead
from datastore.exceptions import NotFoundError
from datastore.queries import (
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
            category = await get_category_by_id(category_id)
            if category is None:
                raise HTTPException(status_code=404, detail="Category not found")
            return category
        if board_id:
            categories = await get_categories_by_board_id(board_id)
            if not categories:
                raise HTTPException(status_code=404, detail="Categories not found")
            return categories

        raise HTTPException(status_code=400, detail="No query parameters provided")
    except NotFoundError as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@category_routes.post("/", response_model=CategoryRead)
async def create_category_endpoint(category: CategoryCreate):
    try:
        category_read: CategoryRead = await create_category(category)
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return category_read


@category_routes.delete("/", status_code=204)
async def delete_category_endpoint(category_id: str = Query(...)):
    try:
        await delete_category(category_id)
    except NotFoundError as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e
