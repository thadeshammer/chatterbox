# datastore/entities/models/user.py
from datetime import datetime
from typing import TYPE_CHECKING, Optional, cast

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import (
        Board,
        Category,
        Comment,
        CommentVote,
        Event,
        EventVote,
        Post,
        PostVote,
        UserProfile,
    )


class UserBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    name: str = Field(..., nullable=False, unique=True)

    user_profile_id: Optional[str] = Field(default=None, nullable=True)

    model_config = cast(
        SQLModelConfig,
        {
            "arbitrary_types_allowed": "True",
            "populate_by_name": "True",
        },
    )


class User(UserBase, table=True):
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.USER), primary_key=True
    )

    boards: list["Board"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    )
    categories: list["Category"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    )
    posts: list["Post"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    )
    comments: list["Comment"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    )
    events: list["Event"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    )
    comment_votes: list["CommentVote"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    )
    post_votes: list["PostVote"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    )
    event_votes: list["EventVote"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    )
    # user_profile: "UserProfile" = Relationship(
    #     back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    # )


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: str = Field(primary_key=True)
