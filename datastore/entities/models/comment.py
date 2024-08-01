# datastore/entities/models/comment.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional, cast

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import Post, User


class CommentBase(SQLModel, table=False):
    content: str = Field(..., min_length=10, max_length=3000, nullable=False)

    approved: bool = Field(default=True)
    approved_at: Optional[datetime] = Field(default=None)
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)

    user_id: str = Field(..., nullable=False, foreign_key="users.id", index=True)
    post_id: str = Field(..., nullable=False, foreign_key="posts.id", index=True)

    model_config = cast(
        SQLModelConfig,
        {
            "arbitrary_types_allowed": "True",
            "populate_by_name": "True",
        },
    )


class Comment(CommentBase, table=True):
    __tablename__ = "comments"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.POST), primary_key=True
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: "User" = Relationship(
        back_populates="comments", sa_relationship_kwargs={"lazy": "subquery"}
    )
    post: "Post" = Relationship(
        back_populates="comments", sa_relationship_kwargs={"lazy": "subquery"}
    )
    votes: list["CommentVote"] = Relationship(
        back_populates="comment", sa_relationship_kwargs={"lazy": "subquery"}
    )


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: str = Field(primary_key=True)
    created_at: datetime = Field()
