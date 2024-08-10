# /datastore/api/board.py
# prefix: /board
import logging
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from datastore.entities.models import BoardCreate, BoardRead
from datastore.exceptions import NotFoundError
from datastore.queries import (
    create_board,
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
        if board_id:
            board = await get_board_by_id(board_id)
            if board is None:
                raise HTTPException(status_code=404, detail="Board not found")
            return board
        if user_id:
            boards = await get_boards_created_by_user_id(user_id)
            if not boards:
                raise HTTPException(status_code=404, detail="Boards not found")
            return boards
        boards = await get_all_boards()
        if not boards:
            raise HTTPException(status_code=404, detail="Boards not found")
        return boards
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@board_routes.post("/", response_model=BoardRead)
async def create_board_endpoint(board: BoardCreate):
    try:
        board_read: BoardRead = await create_board(board)
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return board_read


@board_routes.delete("/", status_code=204)
async def delete_board_endpoint(board_id: str = Query(...)):
    try:
        await delete_board(board_id)
    except NotFoundError as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e
