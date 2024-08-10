# /datastore/api/event.py
# prefix /event
import logging
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from datastore.entities.models import EventCreate, EventRead
from datastore.queries import create_event, get_event_by_id, get_events_by_board_id

event_routes = APIRouter()

logger = logging.getLogger(__name__)


@event_routes.get("/", response_model=Union[EventRead, list[EventRead]])
async def get_events_endpoint(
    event_id: Optional[str] = Query(None),
    board_id: Optional[str] = Query(None),
) -> Union[EventRead, list[EventRead]]:
    try:
        if event_id:
            event = await get_event_by_id(event_id)
            if event is None:
                raise HTTPException(status_code=404, detail="Event not found")
            return event
        elif board_id:
            events = await get_events_by_board_id(board_id)
            if not events:
                raise HTTPException(status_code=404, detail="Events not found")
            return events
        else:
            raise HTTPException(status_code=400, detail="No query parameters provided")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@event_routes.post("/", response_model=EventRead)
async def create_event_endpoint(event: EventCreate):
    try:
        event_read: EventRead = await create_event(event)
    except ValidationError as e:
        logger.error(f"Failed to create event: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return event_read
