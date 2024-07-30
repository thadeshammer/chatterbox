# datastore/entities/models/user.py
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from datastore.entities.ids import EntityId, EntityPrefix


class UserBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    name: str = Field(..., nullable=False, unique=True)

    user_profile_id: Optional[str] = Field(..., nullable=True)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.USER)), primary_key=True
    )


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int = Field(primary_key=True)
