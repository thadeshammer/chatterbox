import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from chatterbox_backend.entities.models import (
    UserCreate,
    UserProfileCreate,
    UserProfileRead,
    UserRead,
)
from chatterbox_backend.exceptions import NotFoundError
from chatterbox_backend.queries import (
    create_user,
    create_user_profile,
    delete_user,
    delete_user_profile,
    get_user_by_id,
    get_user_by_name,
    get_user_profile_by_id,
)

user_routes = APIRouter()

logger = logging.getLogger(__name__)


@user_routes.post("/", response_model=UserRead)
async def create_user_endpoint(user: UserCreate):
    try:
        return await create_user(user)
    except IntegrityError as e:
        if "email" in str(e.orig):
            detail = "A user with this email already exists."
        elif "nick" in str(e.orig):
            detail = "This username is already taken."
        elif "name" in str(e.orig):
            detail = "This nickname is already in use."
        else:
            detail = "A unique constraint violation occurred."

        logger.error(f"Integrity error: {str(e)}")
        raise HTTPException(status_code=409, detail=detail) from e
    except ValidationError as e:
        logger.error(f"Failed to create user: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@user_routes.post("/profile/", response_model=UserProfileRead)
async def create_user_profile_endpoint(user_profile: UserProfileCreate):
    try:
        user_profile_read: UserProfileRead = await create_user_profile(user_profile)
    except ValidationError as e:
        logger.error(f"Failed to create user profile: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e

    return user_profile_read


@user_routes.get("/profile/", response_model=UserProfileRead)
async def get_user_profile_endpoint(
    user_profile_id: str = Query(...),
) -> UserProfileRead:
    try:
        return await get_user_profile_by_id(user_profile_id)
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@user_routes.get("/", response_model=UserRead)
async def get_user_endpoint(
    user_id: Optional[str] = Query(None),
    user_name: Optional[str] = Query(None),
) -> UserRead:
    try:
        if user_id:
            return await get_user_by_id(user_id)
        if user_name:
            return await get_user_by_name(user_name)
        return []
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@user_routes.delete("/", status_code=204)
async def delete_user_endpoint(user_id: str = Query(...)):
    try:
        await delete_user(user_id)
    except NotFoundError as e:
        logger.info(str(e))
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e


@user_routes.delete("/profile/", status_code=204)
async def delete_user_profile_endpoint(user_profile_id: str = Query(...)):
    try:
        await delete_user_profile(user_profile_id)
    except NotFoundError as e:
        logger.info(str(e))
    except ValidationError as e:
        logger.error(f"Validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Server go boom :sad-emoji:") from e
