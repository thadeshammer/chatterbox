# datastore/entities/models/category.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional, cast

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import Board, Post, User


class CategoryBase(SQLModel, table=False):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    title: str = Field(nullable=False, min_length=10, max_length=150)
    description: str = Field(nullable=False, min_length=10, max_length=500)

    locked: bool = Field(default=False)
    locked_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    user_id: str = Field(..., nullable=False, foreign_key="users.id")
    board_id: str = Field(..., nullable=False, foreign_key="boards.id")


class Category(CategoryBase, table=True):
    __tablename__ = "categories"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.CATEGORY), primary_key=True
    )

    user: "User" = Relationship(
        back_populates="categories", sa_relationship_kwargs={"lazy": "subquery"}
    )
    board: "Board" = Relationship(
        back_populates="categories", sa_relationship_kwargs={"lazy": "subquery"}
    )
    posts: list["Post"] = Relationship(
        back_populates="category", sa_relationship_kwargs={"lazy": "subquery"}
    )

    model_config = cast(
        SQLModelConfig,
        {
            "arbitrary_types_allowed": "True",
            "populate_by_name": "True",
        },
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: str = Field(primary_key=True)
