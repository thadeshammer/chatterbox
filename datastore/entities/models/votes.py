# datastore/entities/models/votes.py
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Optional, cast

from pydantic import model_validator
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import Comment, Event, Post, User


class VoteType(StrEnum):
    UP = "up"  # explicit up vote
    # NONE = "none"  # if they vote then un-vote  DO WE NEED THIS??
    DOWN = "down"  # explicit down vote


class _VoteCreate(SQLModel):
    user_id: str = Field(..., nullable=False, foreign_key="users.id")
    vote: str = Field(..., nullable=False)  # TODO enforce adherence to VoteType

    @model_validator(mode="after")
    @classmethod
    def validate_fields(cls, data: "_VoteCreate") -> "_VoteCreate":
        possible_votes = VoteType.__members__.values()
        if data.vote not in possible_votes:
            raise ValueError(f"Invalid value for vote. Use: {possible_votes}")
        return data

    model_config = cast(
        SQLModelConfig,
        {
            "populate_by_name": "True",
        },
    )


class CommentVoteCreate(_VoteCreate):
    comment_id: str = Field(..., nullable=False, foreign_key="comments.id")


class EventVoteCreate(_VoteCreate):
    event_id: str = Field(..., nullable=False, foreign_key="events.id")


class PostVoteCreate(_VoteCreate):
    post_id: str = Field(..., nullable=False, foreign_key="posts.id")


class _VoteBase(SQLModel):
    voted_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)


class CommentVote(_VoteBase, CommentVoteCreate, table=True):
    __tablename__ = "comment_votes"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.COMMENTVOTE),
        primary_key=True,
    )

    user: "User" = Relationship(
        back_populates="comment_votes", sa_relationship_kwargs={"lazy": "subquery"}
    )
    comment: "Comment" = Relationship(
        back_populates="votes", sa_relationship_kwargs={"lazy": "subquery"}
    )


class CommentVoteRead(_VoteBase, CommentVoteCreate):
    id: str = Field(primary_key=True)


class PostVote(_VoteBase, PostVoteCreate, table=True):
    __tablename__ = "post_votes"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.POSTVOTE), primary_key=True
    )

    user: "User" = Relationship(
        back_populates="post_votes", sa_relationship_kwargs={"lazy": "subquery"}
    )
    post: "Post" = Relationship(
        back_populates="votes", sa_relationship_kwargs={"lazy": "subquery"}
    )


class PostVoteRead(_VoteBase, PostVoteCreate):
    id: str = Field(primary_key=True)


class EventVote(_VoteBase, EventVoteCreate, table=True):
    __tablename__ = "event_votes"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.EVENTVOTE), primary_key=True
    )

    user: "User" = Relationship(
        back_populates="event_votes", sa_relationship_kwargs={"lazy": "subquery"}
    )
    event: "Event" = Relationship(
        back_populates="votes", sa_relationship_kwargs={"lazy": "subquery"}
    )


class EventVoteRead(_VoteBase, EventVoteCreate):
    id: str = Field(primary_key=True)
