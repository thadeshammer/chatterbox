# /chatterbox_backend/api/board.py
# prefix: /board
import logging
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from chatterbox_backend.entities.models import BoardCreate, BoardRead, MembershipCreate, UserRole
from chatterbox_backend.exceptions import NotFoundError
from chatterbox_backend.queries import (
    create_board,
    create_membership,
    delete_board,
    get_all_boards,
    get_board_by_id,
    get_boards_created_by_user_id,
)

board_routes = APIRouter()

logger = logging.getLogger(__name__)


@board_routes.get("/", response_model=Union[BoardRead, list[BoardRead]])
async def get_boards_endpoint(
    board_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
) -> Union[BoardRead, list[BoardRead]]:
    try:
        if board_id is not None:
            return await get_board_by_id(board_id)
        if user_id is not None:
            return await get_boards_created_by_user_id(user_id)
        return await get_all_boards()
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@board_routes.post("/", response_model=dict)
async def create_board_endpoint(board: BoardCreate):
    try:
        board_read: BoardRead = await create_board(board)
        membership_create = MembershipCreate(
            user_id=board_read.user_id, board_id=board_read.id, role=UserRole.ADMIN
        )
        membership_read = await create_membership(membership_create)
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return {"board": board_read, "membership": membership_read}


@board_routes.delete("/", status_code=204)
async def delete_board_endpoint(board_id: str = Query(...)):
    try:
        await delete_board(board_id)
    except NotFoundError as e:
        logger.info(str(e))
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e
