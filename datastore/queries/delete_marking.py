# /datastore/queries/delete_marking.py
# TODO figure this out

from datetime import datetime, timezone

from sqlmodel import select

from datastore.db import async_session
from datastore.entities.models import Comment, Event


async def delete_comment(comment_id: str):
    async with async_session() as session:
        async with session.begin():
            query = select(Comment).where(Comment.id == comment_id)
            result = await session.execute(query)
            comment_data = result.scalar_one_or_none()

            if not comment_data:
                raise ValueError(f"Event with id {comment_id} does not exist")

            deleted_at = datetime.now(timezone.utc)

            comment_data.deleted = True
            comment_data.deleted_at = deleted_at

            await session.commit()
        await session.refresh(comment_data)


async def delete_event(event_id: str):
    async with async_session() as session:
        async with session.begin():
            query = select(Event).where(Event.id == event_id)
            result = await session.execute(query)
            event_data = result.scalar_one_or_none()

            if not event_data:
                raise ValueError(f"Event with id {event_id} does not exist")

            deleted_at = datetime.now(timezone.utc)

            event_data.deleted = True
            event_data.deleted_at = deleted_at

            for comment in event_data.comments:
                comment.deleted = True
                comment.deleted_at = deleted_at

            await session.commit()
        await session.refresh(event_data)
