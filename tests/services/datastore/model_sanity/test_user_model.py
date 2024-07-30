import pytest
from sqlmodel import select

from datastore.entities.models import User, UserCreate, UserRead

MOCK_USER_API_REQUEST = {"name": "beeeeegHootie"}


@pytest.mark.asyncio
async def test_create_and_read_user(async_session):
    create_data = UserCreate(**MOCK_USER_API_REQUEST)
    user_data = User(**create_data.model_dump())

    async with async_session.begin():
        async_session.add(user_data)

    await async_session.commit()

    statement = select(User).where(User.name == "beeeeegHootie")
    result = (await async_session.execute(statement)).scalar_one_or_none()

    assert isinstance(result, User)

    user_read = UserRead(**result.model_dump())
    assert user_read.name == "beeeeegHootie"
