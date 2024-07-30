# datastore/entities/ids.py
from enum import StrEnum
from uuid import uuid4


class EntityPrefix(StrEnum):
    ACTION = "action"  # ??
    BOARD = "board"
    CATEGORY = "category"
    COMMENT = "comment"
    COMMENTVOTE = "commentvote"
    EDIT = "edit"
    EVENT = "event"
    EVENTVOTE = "eventvote"
    PIN = "pin"
    POST = "post"
    POSTVOTE = "postvote"
    USER = "user"
    USERPROFILE = "userprofile"


class EntityId:
    def __init__(self, prefix: EntityPrefix):
        self.prefix = prefix
        self.uuid = uuid4()

    def __str__(self):
        return f"{self.prefix}_{self.uuid}"

    def __repr__(self):
        return f"EntityID(prefix={self.prefix}, uuid={self.uuid})"
