# chatterbox_backend/entities/models/user.py
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Optional, cast

from pydantic import EmailStr, StringConstraints, model_validator
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from chatterbox_backend.entities.ids import EntityPrefix, make_entity_id

from .._validator_regexes import LOGIN_NAME_REGEX, NICKNAME_REGEX

if TYPE_CHECKING:
    from . import Board, Category, Comment, Event, Invite, Post, UserProfile


class UserCreate(SQLModel):
    name: Annotated[
        str,
        StringConstraints(min_length=1, max_length=30, pattern=LOGIN_NAME_REGEX),
        Field(..., nullable=False, unique=True, index=True),
    ]
    email: EmailStr = Field(..., nullable=False, unique=True, index=True)
    nickname: Annotated[
        Optional[str],
        StringConstraints(min_length=1, max_length=30, pattern=NICKNAME_REGEX),
        Field(default=None, unique=True, index=True),
    ]

    @model_validator(mode="after")
    @classmethod
    def validate_fields(cls, data: "UserCreate") -> "UserCreate":
        data.name = data.name.lower()
        data.email = data.email.lower()
        if data.nickname is None:
            data.nickname = data.name

        return data

    model_config = cast(
        SQLModelConfig,
        {
            "populate_by_name": "True",
        },
    )


class UserBase(UserCreate):
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.USER), primary_key=True
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    boards: list["Board"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    )
    memberships: list["Membership"] = Relationship(
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
    user_profile: "UserProfile" = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    )
    invites: list["Invite"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "subquery"}
    )


class UserRead(UserBase):
    id: str = Field(primary_key=True)
    created_at: datetime = Field()


class UserUpdate(SQLModel):
    """NOTE changing user name or email could be tricky, we'll wire it up later"""

    nickname: Annotated[
        Optional[str],
        StringConstraints(min_length=1, max_length=30, pattern=NICKNAME_REGEX),
        Field(default=None, nullable=False, unique=True, index=True),
    ]

    @model_validator(mode="after")
    @classmethod
    def at_least_one_isnt_none(cls, data: "UserUpdate") -> "UserUpdate":
        if not any(value is not None for value in data.model_dump().values()):
            raise ValueError("All update fields are None.")
        return data
