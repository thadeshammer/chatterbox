# datastore/entities/models/votes.py
from datetime import datetime
from enum import StrEnum

from datastore.entities.ids import EntityId, EntityPrefix
from sqlmodel import Field, SQLModel


class VoteType(StrEnum):
    UP = "up"  # explicit up vote
    NONE = "none"  # if they vote then un-vote
    DOWN = "down"  # explicit down vote


class VoteBase(SQLModel, table=False):
    vote: str = Field(..., nullable=False)
    voted_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class CommentVote(VoteBase, table=True):
    __tablename__: str = "comment_votes"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.COMMENTVOTE)),
        primary_key=True,
    )

    comment_id: str = Field(..., nullable=False, foreign_key="comments.id")


class CommentVoteCreate(CommentVote):
    pass


class CommentVoteRead(CommentVote):
    pass


class PostVote(VoteBase, table=True):
    __tablename__: str = "post_votes"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.POSTVOTE)), primary_key=True
    )

    post_id: str = Field(..., nullable=False, foreign_key="posts.id")


class PostVoteCreate(PostVote):
    pass


class PostVoteRead(PostVote):
    pass


class EventVote(VoteBase, table=True):
    __tablename__: str = "event_votes"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.EVENTVOTE)), primary_key=True
    )

    event_id: str = Field(..., nullable=False, foreign_key="events.id")


class EventVoteCreate(EventVote):
    pass


class EventVoteRead(EventVote):
    pass
