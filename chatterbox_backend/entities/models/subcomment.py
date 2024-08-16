# chatterbox_backend/entities/models/subcomment.py
"""Subcomment Data Model

Subcomments are child-comments to one parent-comment; supports Discord or FB-style
tangent threads within a single comment in a post.
"""
from datetime import datetime
from typing import TYPE_CHECKING, Optional, cast

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from chatterbox_backend.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import Comment, User


class SubcommentCreate(SQLModel):
    content: str = Field(..., min_length=1, max_length=3000, nullable=False)
    user_id: str = Field(..., nullable=False, foreign_key="users.id", index=True)
    comment_id: str = Field(..., nullable=False, foreign_key="comment.id", index=True)

    model_config = cast(
        SQLModelConfig,
        {
            "populate_by_name": "True",
        },
    )


class SubcommentBase(SubcommentCreate):
    approved: bool = Field(default=True)
    approved_at: Optional[datetime] = Field(default=None)
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)


class Subcomment(SubcommentBase, table=True):
    __tablename__ = "subcomments"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.SUBCOMMENT),
        primary_key=True,
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: "User" = Relationship(
        back_populates="subcomments", sa_relationship_kwargs={"lazy": "subquery"}
    )
    comment: "Comment" = Relationship(
        back_populates="subcomments", sa_relationship_kwargs={"lazy": "subquery"}
    )


class SubcommentRead(SubcommentBase):
    id: str = Field(primary_key=True)
    created_at: datetime = Field()
