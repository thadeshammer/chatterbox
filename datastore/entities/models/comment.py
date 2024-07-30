# datastore/entities/models/comment.py
from datetime import datetime
from typing import Optional

from datastore.entities.ids import EntityId, EntityPrefix
from sqlmodel import Field, SQLModel


class CommentBase(SQLModel, table=False):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    content: str = Field(..., min_length=10, max_length=3000, nullable=False)

    approved: bool = Field(default=True)
    approved_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )

    user_id: str = Field(..., nullable=False, foreign_key="users.id", index=True)
    post_id: str = Field(..., nullable=False, foreign_key="posts.id", index=True)


class Comment(CommentBase, table=True):
    __tablename__: str = "comments"

    id: str = Field(
        default_factory=lambda: str(EntityId(EntityPrefix.POST)), primary_key=True
    )


class CommentCreate(Comment):
    pass


class CommentRead(Comment):
    pass
