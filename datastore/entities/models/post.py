# datastore/entities/models/post.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional, cast

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import Category, Comment, PostVote, User


class PostBase(SQLModel, table=False):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    title: str = Field(nullable=False, min_length=10, max_length=150)
    content: str = Field(nullable=False, min_length=10, max_length=3000)

    locked: bool = Field(default=False)
    locked_at: Optional[datetime] = Field(default=None)
    approved: bool = Field(default=True)
    approved_at: Optional[datetime] = Field(default=None)
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)

    user_id: str = Field(..., nullable=False, foreign_key="users.id")
    category_id: str = Field(..., nullable=False, foreign_key="categories.id")

    model_config = cast(
        SQLModelConfig,
        {
            "arbitrary_types_allowed": "True",
            "populate_by_name": "True",
        },
    )


class Post(PostBase, table=True):
    __tablename__ = "posts"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.POST), primary_key=True
    )

    user: "User" = Relationship(
        back_populates="posts", sa_relationship_kwargs={"lazy": "subquery"}
    )
    category: "Category" = Relationship(
        back_populates="posts", sa_relationship_kwargs={"lazy": "subquery"}
    )
    comments: "Comment" = Relationship(
        back_populates="post", sa_relationship_kwargs={"lazy": "subquery"}
    )
    votes: list["PostVote"] = Relationship(
        back_populates="post", sa_relationship_kwargs={"lazy": "subquery"}
    )


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: str = Field(primary_key=True)