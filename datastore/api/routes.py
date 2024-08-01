import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from datastore.db.query import (
    create_board,
    create_user,
    get_user_by_id,
    get_user_by_name,
)
from datastore.entities.models import BoardCreate, BoardRead, UserCreate, UserRead

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
