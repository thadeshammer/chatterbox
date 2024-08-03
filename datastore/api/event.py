# /datastore/api/event.py
# prefix /event
import logging

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from datastore.entities.models import EventCreate, EventRead
from datastore.queries import create_event, get_event_by_id

event_routes = APIRouter()

logger = logging.getLogger(__name__)


@event_routes.get("/{event_id}", response_model=EventRead)
async def get_event_endpoint(event_id: str) -> EventRead:
    try:
        event = await get_event_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return event


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
