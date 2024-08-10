# datastore/entities/models/category.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional, cast

from pydantic import model_validator
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import Board, Post, User


class CategoryCreate(SQLModel):
    name: str = Field(nullable=False, min_length=3, max_length=150)
    description: str = Field(nullable=False, min_length=5, max_length=500)

    user_id: str = Field(..., nullable=False, foreign_key="users.id")
    board_id: str = Field(..., nullable=False, foreign_key="boards.id", index=True)

    model_config = cast(
        SQLModelConfig,
        {
            "populate_by_name": "True",
        },
    )


class CategoryBase(CategoryCreate):
    locked: bool = Field(default=False)
    locked_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Category(CategoryBase, table=True):
    __tablename__ = "categories"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.CATEGORY), primary_key=True
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: "User" = Relationship(
        back_populates="categories", sa_relationship_kwargs={"lazy": "subquery"}
    )
    board: "Board" = Relationship(
        back_populates="categories", sa_relationship_kwargs={"lazy": "subquery"}
    )
    posts: list["Post"] = Relationship(
        back_populates="category", sa_relationship_kwargs={"lazy": "subquery"}
    )


class CategoryRead(CategoryBase):
    id: str = Field(primary_key=True)
    created_at: datetime = Field()


class CategoryUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=150)
    description: Optional[str] = Field(default=None, min_length=5, max_length=500)

    @model_validator(mode="after")
    @classmethod
    def at_least_one_isnt_none(cls, data: "CategoryUpdate") -> "CategoryUpdate":
        if not any(value is not None for value in data.model_dump().values()):
            raise ValueError("All update fields are None.")
        return data
