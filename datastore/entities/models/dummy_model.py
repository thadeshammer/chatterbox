# datastore/entities/models/dummy_model.py
# Just for smoketesting the DS in dire consequences
from sqlmodel import Field, SQLModel


class DummyModel(SQLModel, table=True):
    # Simplistic model for sanity tests
    # Has to live here because Pytest and SQLModel are VERY fussy together.
    __tablename__: str = "dummy_models"

    id: int = Field(default_factory=int, primary_key=True)

    name: str = Field(default=None)
    value: int = Field(default=None)
