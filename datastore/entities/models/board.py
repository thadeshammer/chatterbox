# datastore/entities/models/board.py
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from datastore.entities.ids import EntityId, EntityPrefix


class BoardBase(SQLModel, table=False):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    title: str = Field(nullable=False, min_length=10, max_length=150)
    description: str = Field(nullable=False, min_length=10, max_length=500)

    locked: bool = Field(default=False)
    locked_at: Optional[datetime] = Field(default=None)
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)

    user_id: str = Field(..., nullable=False, foreign_key="users.id")


class Board(BoardBase, table=True):
    __tablename__ = "boards"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.BOARD)), primary_key=True
    )


class BoardCreate(BoardBase):
    pass


class BoardRead(BoardBase):
    id: str = Field(primary_key=True)
