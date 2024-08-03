# datastore/entities/ids.py
from enum import StrEnum
from uuid import uuid4


class EntityPrefix(StrEnum):
    ACTION = "action"  # ??
    BOARD = "board"
    CATEGORY = "category"
    COMMENT = "comment"
    # COMMENTVOTE = "commentvote"
    EDIT = "edit"
    EVENT = "event"
    # EVENTVOTE = "eventvote"
    INVITE = "invite"
    MEMBERSHIP = "membership"
    PIN = "pin"
    POST = "post"
    # POSTVOTE = "postvote"
    USER = "user"
    USERPROFILE = "userprofile"


def make_entity_id(prefix: EntityPrefix) -> str:
    return f"{prefix}-{str(uuid4())}"
