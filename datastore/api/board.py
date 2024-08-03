# /datastore/api/board.py
# prefix: /board
import logging

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from datastore.entities.models import BoardCreate, BoardRead
from datastore.queries import create_board, get_board_by_id

board_routes = APIRouter()

logger = logging.getLogger(__name__)


@board_routes.get("/{board_id}", response_model=BoardRead)
async def get_board_endpoint(board_id: str) -> BoardRead:
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


@board_routes.get("/user/{user_id}", response_model=list[BoardRead])
async def get_boards_by_user_id_endpoint(user_id: str) -> list[BoardRead]:
    pass


@board_routes.post("/", response_model=BoardRead)
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
