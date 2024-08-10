# datastore/entities/models/board.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional, cast

from pydantic import model_validator
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import Category, Event, Invite, User


class BoardCreate(SQLModel):
    name: str = Field(..., nullable=False, min_length=3, max_length=150)
    description: str = Field(..., nullable=False, min_length=5, max_length=500)
    user_id: str = Field(..., nullable=False, foreign_key="users.id")

    model_config = cast(
        SQLModelConfig,
        {
            "populate_by_name": "True",
        },
    )


class BoardBase(BoardCreate):
    locked: bool = Field(default=False)
    locked_at: Optional[datetime] = Field(default=None)
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)


class Board(BoardBase, table=True):
    __tablename__ = "boards"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.BOARD), primary_key=True
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: "User" = Relationship(
        back_populates="boards", sa_relationship_kwargs={"lazy": "subquery"}
    )
    categories: list["Category"] = Relationship(
        back_populates="board", sa_relationship_kwargs={"lazy": "subquery"}
    )
    events: list["Event"] = Relationship(
        back_populates="board", sa_relationship_kwargs={"lazy": "subquery"}
    )
    members: list["Membership"] = Relationship(
        back_populates="board", sa_relationship_kwargs={"lazy": "subquery"}
    )
    invites: list["Invite"] = Relationship(
        back_populates="board", sa_relationship_kwargs={"lazy": "subquery"}
    )


class BoardRead(BoardBase):
    id: str = Field(primary_key=True)
    created_at: datetime = Field()


class BoardUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=150)
    description: Optional[str] = Field(default=None, min_length=5, max_length=500)

    @model_validator(mode="after")
    @classmethod
    def at_least_one_isnt_none(cls, data: "BoardUpdate") -> "BoardUpdate":
        if not any(value is not None for value in data.model_dump().values()):
            raise ValueError("All update fields are None.")
        return data
