# datastore/entities/models/board.py
from datetime import datetime
from typing import Optional

from datastore.entities.ids import EntityId, EntityPrefix
from sqlmodel import Field, SQLModel


class BoardBase(SQLModel, table=False):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    title: str = Field(nullable=False, min_length=10, max_length=150)
    description: str = Field(nullable=False, min_length=10, max_length=500)

    locked: bool = Field(default=False)
    locked_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )

    user_id: str = Field(..., nullable=False, foreign_key="users.id")

    # board


class Board(BoardBase, table=True):
    __tablename__: str = "boards"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.BOARD)), primary_key=True
    )


class BoardCreate(Board):
    pass


class BoardRead(Board):
    pass
