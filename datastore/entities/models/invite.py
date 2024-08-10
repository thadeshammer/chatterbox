# datastore/entities/models/post.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional, cast

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import User


class InviteCreate(SQLModel):
    email: EmailStr = Field(..., nullable=False, index=True)
    board_id: str = Field(..., nullable=False, foreign_key="boards.id", index=True)
    issuing_user_id: str = Field(..., nullable=False, foreign_key="users.id")

    model_config = cast(
        SQLModelConfig,
        {
            "populate_by_name": "True",
        },
    )


class InviteBase(InviteCreate):
    accepted_at: Optional[datetime] = Field(default=None)


class Invite(InviteBase, table=True):
    __tablename__ = "invites"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.Invite),
        primary_key=True,
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: "User" = Relationship(
        back_populates="invites", sa_relationship_kwargs={"lazy": "subquery"}
    )
    board: "Board" = Relationship(
        back_populates="invites", sa_relationship_kwargs={"lazy": "subquery"}
    )


class InviteRead(InviteBase):
    id: str = Field(primary_key=True)
    created_at: datetime = Field()
