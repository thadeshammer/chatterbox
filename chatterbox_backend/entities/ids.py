# chatterbox_backend/entities/ids.py
from enum import StrEnum
from uuid import uuid4


class EntityPrefix(StrEnum):
    ACTION = "action"  # ??
    BOARD = "board"
    CATEGORY = "category"
    COMMENT = "comment"
    EDIT = "edit"
    EVENT = "event"
    INVITE = "invite"
    MEMBERSHIP = "membership"
    PIN = "pin"
    POST = "post"
    SUBCOMMENT = "subcomment"
    USER = "user"
    USERPROFILE = "userprofile"


def make_entity_id(prefix: EntityPrefix) -> str:
    return f"{prefix}-{str(uuid4())}"
