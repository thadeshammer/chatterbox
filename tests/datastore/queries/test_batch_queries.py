import asyncio

import pytest

from datastore.entities.models import (
    BoardCreate,
    BoardRead,
    CategoryCreate,
    CategoryRead,
    UserCreate,
    UserRead,
)
from datastore.queries import (
    create_board,
    create_category,
    create_user,
    get_categories_by_board_id,
)


async def test_get_categories_by_board_id():
    user_create = UserCreate(name="test_name", email="testemail@example.com")
    user_read: UserRead = await create_user(user_create)

    board_create = BoardCreate(
        name="test_name",
        description="describing things",
        user_id=user_read.id,
    )
    board_read: BoardRead = await create_board(board_create)
    assert board_read.name == board_create.name

    tasks = []
    for name in range(3):
        category_create = CategoryCreate(
            name=f"test{name}",
            description=f"describing things {name}",
            user_id=user_read.id,
            board_id=board_read.id,
        )
        tasks.append(create_category(category_create))

    await asyncio.gather(*tasks)

    categories = await get_categories_by_board_id(board_read.id)

    names = [category.name for category in categories]

    assert "test0" in names
    assert "test1" in names
    assert "test2" in names
