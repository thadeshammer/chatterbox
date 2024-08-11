from functools import wraps
from typing import Callable

from fastapi import HTTPException, Request

from chatterbox_backend.entities.models import MembershipRead, User, UserRole
from chatterbox_backend.exceptions import NotFoundError
from chatterbox_backend.queries import get_membership


def get_current_user() -> User:
    pass


async def check_membership_role(user_id: str, board_id: str, required_role: UserRole):
    membership: MembershipRead = await get_membership(user_id, board_id)
    if membership is None:
        raise NotFoundError(f"{user_id} is not a member of {board_id}")

    if membership.role >= required_role:
        return True

    return False


def role_required(required_role: UserRole):
    """Decorator for endpoint auth checks.

    e.g. using fastapi.Depends

        @post_routes.post("/", response_model=PostRead)
        @role_required(UserRole.USER)
        async def create_post_endpoint(post: PostCreate, request: Request):

    Args:
        required_role (UserRole): The minimum role required for a given action.
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            user_id = (
                request.state.user_id
            )  # Assume user_id is stored here, adapt as necessary
            board_id = kwargs.get(
                "board_id"
            )  # Assume board_id is passed as a keyword argument

            if not await check_membership_role(user_id, board_id, required_role):
                raise HTTPException(
                    status_code=403,
                    detail="You do not have the necessary permissions to perform this action.",
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator
