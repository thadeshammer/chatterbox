# datastore/entities/models/category.py
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from datastore.entities.ids import EntityId, EntityPrefix


class CategoryBase(SQLModel, table=False):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    title: str = Field(nullable=False, min_length=10, max_length=150)
    description: str = Field(nullable=False, min_length=10, max_length=500)

    locked: bool = Field(default=False)
    locked_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    user_id: str = Field(..., nullable=False, foreign_key="users.id")

    # board


class Category(CategoryBase, table=True):
    __tablename__ = "categories"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.CATEGORY)), primary_key=True
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: str = Field(primary_key=True)
