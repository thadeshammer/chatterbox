# datastore/entities/models/post.py
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from datastore.entities.ids import EntityId, EntityPrefix


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


class Event(EventBase, table=True):
    __tablename__ = "events"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.POST)), primary_key=True
    )


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: str = Field(primary_key=True)
