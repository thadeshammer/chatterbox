# datastore/entities/models/post.py
from datetime import datetime
from typing import Optional

from datastore.entities.ids import EntityId, EntityPrefix
from sqlmodel import Field, SQLModel


class PostBase(SQLModel, table=False):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    title: str = Field(nullable=False, min_length=10, max_length=150)
    content: str = Field(nullable=False, min_length=10, max_length=3000)

    locked: bool = Field(default=False)
    locked_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    approved: bool = Field(default=True)
    approved_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )

    user_id: str = Field(..., nullable=False, foreign_key="users.id")
    category_id: str = Field(..., nullable=False, foreign_key="categories.id")


class Post(PostBase, table=True):
    __tablename__: str = "posts"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.POST)), primary_key=True
    )


class PostCreate(Post):
    pass


class PostRead(Post):
    pass
