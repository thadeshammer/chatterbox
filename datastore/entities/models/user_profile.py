# datastore/entities/models/user_profile.py
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional, cast

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig

from datastore.entities.ids import EntityPrefix, make_entity_id

if TYPE_CHECKING:
    from . import User


class UserProfileBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user_id: str = Field(..., nullable=False, foreign_key="users.id")

    # user: "User" = Relationship(
    #     back_populates="user_profile", sa_relationship_kwargs={"lazy": "subquery"}
    # )

    # birthday: Optional[date] = Field(default=None, nullable=True)
    # TODO more profile stuff

    model_config = cast(
        SQLModelConfig,
        {
            "arbitrary_types_allowed": "True",
            "populate_by_name": "True",
        },
    )


class UserProfile(UserProfileBase, table=True):
    """User profile info, to be expanded upon."""

    __tablename__ = "user_profiles"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.USERPROFILE),
        primary_key=True,
    )


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileRead(UserProfileBase):
    id: str = Field(primary_key=True)
