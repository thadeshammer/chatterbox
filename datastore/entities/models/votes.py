# datastore/entities/models/votes.py
from datetime import datetime
from enum import StrEnum
from typing import Optional

from sqlmodel import Field, SQLModel

from datastore.entities.ids import EntityId, EntityPrefix


class VoteType(StrEnum):
    UP = "up"  # explicit up vote
    NONE = "none"  # if they vote then un-vote
    DOWN = "down"  # explicit down vote


class VoteBase(SQLModel, table=False):
    vote: str = Field(..., nullable=False)  # TODO enforce adherence to VoteType
    voted_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)


class CommentVote(VoteBase, table=True):
    __tablename__ = "comment_votes"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.COMMENTVOTE)),
        primary_key=True,
    )

    comment_id: str = Field(..., nullable=False, foreign_key="comments.id")


class CommentVoteCreate(VoteBase):
    pass


class CommentVoteRead(VoteBase):
    id: int = Field(primary_key=True)


class PostVote(VoteBase, table=True):
    __tablename__ = "post_votes"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.POSTVOTE)), primary_key=True
    )

    post_id: str = Field(..., nullable=False, foreign_key="posts.id")


class PostVoteCreate(VoteBase):
    pass


class PostVoteRead(VoteBase):
    id: int = Field(primary_key=True)


class EventVote(VoteBase, table=True):
    __tablename__ = "event_votes"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.EVENTVOTE)), primary_key=True
    )

    event_id: str = Field(..., nullable=False, foreign_key="events.id")


class EventVoteCreate(VoteBase):
    pass


class EventVoteRead(VoteBase):
    id: int = Field(primary_key=True)
