# datastore/entities/models/user_profile.py
from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from datastore.entities.ids import EntityId, EntityPrefix


class UserProfileBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    birthday: Optional[date] = Field(default=None, nullable=True)
    # TODO more stuff


class UserProfile(UserProfileBase, table=True):
    """User profile info, to be expanded upon."""

    __tablename__ = "user_profiles"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.USERPROFILE)),
        primary_key=True,
    )


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileRead(UserProfileBase):
    id: int = Field(primary_key=True)
