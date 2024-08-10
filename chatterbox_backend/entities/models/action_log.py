from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from chatterbox_backend.entities.ids import EntityPrefix, make_entity_id


class ActionLogCreate(SQLModel):
    endpoint: str = Field(..., index=True)
    parameters: str = Field(...)


class ActionLogBase(ActionLogCreate):
    success: bool = Field(default=False)
    error_message: Optional[str] = Field(default=None)


class ActionLog(ActionLogBase, table=True):
    __tablename__ = "action_logs"

    id: str = Field(
        default_factory=lambda: make_entity_id(EntityPrefix.ACTION), primary_key=True
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class ActionLogRead(ActionLogBase):
    id: str
    created_at: datetime
