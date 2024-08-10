# /chatterbox_backend/api/invite.py
# prefix: /invite
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from chatterbox_backend.entities.models import InviteCreate, InviteRead
from chatterbox_backend.exceptions import NotFoundError
from chatterbox_backend.queries import (
    create_invite,
    delete_invite,
    get_invites_by_board_id,
    get_invites_by_email,
    get_invites_by_user_id,
)

invite_routes = APIRouter()

logger = logging.getLogger(__name__)


@invite_routes.post("/", response_model=InviteRead)
async def create_invite_endpoint(invite: InviteCreate):
    logger.debug(f"{invite=}")
    try:
        return await create_invite(invite)
    except ValidationError as e:
        logger.error(f"Failed to create user: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@invite_routes.delete("/", response_model=InviteRead)
async def delete_invite_endpoint(invite_id: str = Query(...)):
    try:
        return await delete_invite(invite_id)
    except NotFoundError as e:
        logger.info(str(e))
    except ValidationError as e:
        logger.error(f"Failed to create user: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@invite_routes.get("/", response_model=list[InviteRead])
async def get_invites_endpoint(
    board_id: str = Query(...), user_id: str = Query(...), email: str = Query(...)
):
    try:
        if board_id is not None:
            return await get_invites_by_board_id(board_id)
        if user_id is not None:
            return await get_invites_by_user_id(user_id)
        if email is not None:
            return await get_invites_by_email(email)
        return []
    except ValidationError as e:
        logger.error(f"Failed to create user: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e
