# datastore/entities/models/board.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional, cast

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import Category, Event, User


class BoardCreate(SQLModel):
    title: str = Field(..., nullable=False, min_length=10, max_length=150)
    description: str = Field(..., nullable=False, min_length=10, max_length=500)
    user_id: str = Field(..., nullable=False, foreign_key="users.id")

    model_config = cast(
        SQLModelConfig,
        {
            # "arbitrary_types_allowed": "True",
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


class BoardRead(BoardBase):
    id: str = Field(primary_key=True)
    created_at: datetime = Field()
