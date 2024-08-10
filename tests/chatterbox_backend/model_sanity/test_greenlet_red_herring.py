import pytest
from sqlmodel import select

from chatterbox_backend.entities.models import Board, Category, Comment, Post, User


@pytest.mark.asyncio
async def test_greenlet_red_herring(async_session):
    # VERY often this error is caused by subsequent references to a SQLModel table model member
    # after it's been committed to the DB. For example, if you add and commit a UserData then
    # immediately after, you reference user_data.id, it MIGHT be okay, but often what will happen is
    # an unintended I/O hit here, where it checks to make sure some other thread didn't update the
    # value underneath your transaction. The fix is either to close out and make a new transaction
    # or, if you know (for instance) the immutable ID won't change, you can store it locally just
    # before committing it. Just make sure to invalidate it / not use it if the transaction bombs
    # out.

    # Another cause (and the reason this "test" exists) is that your relationships are incorrectly
    # defined, in which case the greenlet spawn error is a red herring and covering up the truth on
    # you. If you turn on DEBUG logging for SQLAlchemy (see chatterbox_backend.py logging setup) you can
    # execute this test and look at the output to see if any of your nested relationships are bogus.
    # See: https://stackoverflow.com/a/77610445/19677371
    await async_session.execute(select(Board))
    await async_session.execute(select(Category))
    await async_session.execute(select(Comment))
    await async_session.execute(select(Post))
    await async_session.execute(select(User))
