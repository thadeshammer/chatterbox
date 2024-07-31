# datastore/entities/models/dummy_model.py
# Just for smoketesting the DS in dire consequences
from sqlmodel import Field, SQLModel


class DummyModelBase(SQLModel, table=False):
    name: str = Field(default=None)
    value: int = Field(default=None)


class DummyModel(DummyModelBase, table=True):
    # Simplistic model for sanity tests
    # Has to live here because Pytest and SQLModel are VERY fussy together.
    __tablename__ = "dummy_models"

    id: str = Field(default_factory=int, primary_key=True)


class DummyModelCreate(DummyModelBase):
    pass


class DummyModelRead(DummyModelBase):
    id: str = Field(primary_key=True)
