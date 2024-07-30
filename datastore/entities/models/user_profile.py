# datastore/entities/models/user_profile.py
from datetime import date, datetime
from typing import Optional

from datastore.entities.ids import EntityId, EntityPrefix
from sqlmodel import Field, SQLModel


class UserProfileBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    birthday: Optional[date] = Field(nullable=True)
    # TODO more stuff


class UserProfile(UserProfileBase, table=True):
    __tablename__: str = "user_profiles"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.USERPROFILE)),
        primary_key=True,
    )


class UserProfileCreate(UserProfile):
    pass


class UserProfileRead(UserProfile):
    pass
