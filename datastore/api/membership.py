# /datastore/api/membership.py
# prefix: /membership
import logging
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from datastore.entities.models import MembershipRead
from datastore.queries import get_memberships_by_board_id, get_memberships_by_user_id

membership_routes = APIRouter()

logger = logging.getLogger(__name__)


@membership_routes.get("/", response_model=list[MembershipRead])
async def get_memberships_endpoint(
    board_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
) -> list[MembershipRead]:
    try:
        if board_id:
            memberships = await get_memberships_by_board_id(board_id)
            if not memberships:
                raise HTTPException(
                    status_code=404, detail="No memberships found for this board"
                )
        elif user_id:
            memberships = await get_memberships_by_user_id(user_id)
            if not memberships:
                raise HTTPException(
                    status_code=404, detail="No memberships found for this user"
                )
        else:
            raise HTTPException(status_code=400, detail="No query parameters provided")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return memberships
