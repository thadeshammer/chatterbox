# /chatterbox_backend/api/event.py
# prefix /event
import logging
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from chatterbox_backend.entities.models import EventCreate, EventRead
from chatterbox_backend.exceptions import NotFoundError
from chatterbox_backend.queries import (
    create_event,
    delete_event,
    get_event_by_id,
    get_events_by_board_id,
)

event_routes = APIRouter()

logger = logging.getLogger(__name__)


@event_routes.get("/", response_model=Union[EventRead, list[EventRead]])
async def get_events_endpoint(
    event_id: Optional[str] = Query(None),
    board_id: Optional[str] = Query(None),
) -> Union[EventRead, list[EventRead]]:
    try:
        if event_id:
            return await get_event_by_id(event_id)
        if board_id:
            return await get_events_by_board_id(board_id)
        return []
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@event_routes.post("/", response_model=EventRead)
async def create_event_endpoint(event: EventCreate):
    try:
        return await create_event(event)
    except ValidationError as e:
        logger.error(f"Failed to create event: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@event_routes.delete("/", status_code=204)
async def delete_event_endpoint(event_id: str = Query(...)):
    try:
        await delete_event(event_id)
    except NotFoundError as e:
        logger.info(str(e))
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e
