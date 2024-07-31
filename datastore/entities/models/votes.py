# datastore/entities/models/votes.py
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import Comment, Event, Post, User


class VoteType(StrEnum):
    UP = "up"  # explicit up vote
    NONE = "none"  # if they vote then un-vote
    DOWN = "down"  # explicit down vote


class VoteBase(SQLModel, table=False):
    vote: str = Field(..., nullable=False)  # TODO enforce adherence to VoteType
    voted_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user_id: str = Field(..., nullable=False, foreign_key="users.id")

    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)


class CommentVote(VoteBase, table=True):
    __tablename__ = "comment_votes"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.COMMENTVOTE),
        primary_key=True,
    )

    comment_id: str = Field(..., nullable=False, foreign_key="comments.id")
    user: "User" = Relationship(
        back_populates="comment_votes", sa_relationship_kwargs={"lazy": "subquery"}
    )
    comment: "Comment" = Relationship(
        back_populates="votes", sa_relationship_kwargs={"lazy": "subquery"}
    )


class CommentVoteCreate(VoteBase):
    pass


class CommentVoteRead(VoteBase):
    id: str = Field(primary_key=True)


class PostVote(VoteBase, table=True):
    __tablename__ = "post_votes"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.POSTVOTE), primary_key=True
    )

    post_id: str = Field(..., nullable=False, foreign_key="posts.id")
    user: "User" = Relationship(
        back_populates="post_votes", sa_relationship_kwargs={"lazy": "subquery"}
    )
    post: "Post" = Relationship(
        back_populates="votes", sa_relationship_kwargs={"lazy": "subquery"}
    )


class PostVoteCreate(VoteBase):
    pass


class PostVoteRead(VoteBase):
    id: str = Field(primary_key=True)


class EventVote(VoteBase, table=True):
    __tablename__ = "event_votes"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.EVENTVOTE), primary_key=True
    )

    event_id: str = Field(..., nullable=False, foreign_key="events.id")
    user: "User" = Relationship(
        back_populates="event_votes", sa_relationship_kwargs={"lazy": "subquery"}
    )
    event: "Event" = Relationship(
        back_populates="votes", sa_relationship_kwargs={"lazy": "subquery"}
    )


class EventVoteCreate(VoteBase):
    pass


class EventVoteRead(VoteBase):
    id: str = Field(primary_key=True)
