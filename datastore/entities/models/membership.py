# datastore/entities/models/post.py
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, cast

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import Board, User


class UserRole(StrEnum):
    NORMAL = "normal"
    MODERATOR = "moderator"
    ADMIN = "admin"


class MembershipCreate(SQLModel):
    user_id: str = Field(..., nullable=False, foreign_key="users.id", index=True)
    board_id: str = Field(..., nullable=False, foreign_key="boards.id", index=True)
    role: str = Field(default=UserRole.NORMAL, nullable=False)

    model_config = cast(
        SQLModelConfig,
        {
            "populate_by_name": "True",
        },
    )


class MembershipBase(MembershipCreate):
    pass


class Membership(MembershipBase, table=True):
    __tablename__ = "memberships"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.MEMBERSHIP),
        primary_key=True,
    )
    joined_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: "User" = Relationship(
        back_populates="memberships", sa_relationship_kwargs={"lazy": "subquery"}
    )
    board: "Board" = Relationship(
        back_populates="members", sa_relationship_kwargs={"lazy": "subquery"}
    )


class MembershipRead(MembershipBase):
    id: str = Field(primary_key=True)
    joined_at: datetime = Field()
