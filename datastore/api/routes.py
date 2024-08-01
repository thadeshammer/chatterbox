import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from datastore.db.query import create_user, get_user_by_id, get_user_by_name
from datastore.entities.models import UserCreate, UserRead

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/user/", response_model=UserRead)
async def create_user_endpoint(user: UserCreate):
    try:
        await create_user(user)
    except ValidationError as e:
        logger.error(f"Failed to create user: validation error. {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error.") from e

    return {"message": "ok."}


@router.get("/users/", response_model=UserRead)
async def get_user(
    user_id: Optional[str] = Query(None), user_name: Optional[str] = Query(None)
):
    try:
        if user_id:
            user = await get_user_by_id(user_id)
        elif user_name:
            user = await get_user_by_name(user_name)
        else:
            raise HTTPException(
                status_code=400, detail="Either user_id or user_name must be provided"
            )

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    except ValidationError as e:
        logger.error(f"Failed validation: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed validation.") from e
    except Exception as e:
        logger.error(f"Ask Thades what happened I guess. {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error.") from e

    return user
