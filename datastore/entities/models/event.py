# datastore/entities/models/event.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional, cast

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import Board, EventVote, User


class EventBase(SQLModel, table=False):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    title: str = Field(nullable=False, min_length=10, max_length=150)
    content: str = Field(nullable=False, min_length=10, max_length=3000)

    locked: bool = Field(default=False)
    locked_at: Optional[datetime] = Field(default=None)
    approved: bool = Field(default=True)
    approved_at: Optional[datetime] = Field(default=None)
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)

    user_id: str = Field(..., nullable=False, foreign_key="users.id")
    board_id: str = Field(..., nullable=False, foreign_key="boards.id")

    model_config = cast(
        SQLModelConfig,
        {
            "arbitrary_types_allowed": "True",
            "populate_by_name": "True",
        },
    )


class Event(EventBase, table=True):
    __tablename__ = "events"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.POST), primary_key=True
    )

    user: "User" = Relationship(
        back_populates="events", sa_relationship_kwargs={"lazy": "subquery"}
    )
    board: "Board" = Relationship(
        back_populates="events", sa_relationship_kwargs={"lazy": "subquery"}
    )
    votes: list["EventVote"] = Relationship(
        back_populates="event", sa_relationship_kwargs={"lazy": "subquery"}
    )


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: str = Field(primary_key=True)