# /datastore/api/membership.py
# prefix: /membership
import logging

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from datastore.entities.models import MembershipCreate, MembershipRead
from datastore.queries import get_memberships_by_board_id, get_memberships_by_user_id

membership_routes = APIRouter()

logger = logging.getLogger(__name__)


@membership_routes.get("/board/{board_id}", response_model=list[MembershipRead])
async def get_memberships_by_board_endpoint(board_id: str) -> list[MembershipRead]:
    try:
        memberships = await get_memberships_by_board_id(board_id)
        if memberships is None:
            raise HTTPException(status_code=404, detail="Board not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return memberships


@membership_routes.get("/user/{user_id}", response_model=list[MembershipRead])
async def get_memberships_by_user_endpoint(user_id: str) -> list[MembershipRead]:
    try:
        memberships = await get_memberships_by_user_id(user_id)
        if memberships is None:
            raise HTTPException(status_code=404, detail="Board not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return memberships
