from uuid import  UUID

from sqlalchemy import select, CursorResult
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from kafka_event_shema import kafka_event

from models import InboxModel

class InboxRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_if_new(self, inbox: kafka_event) -> bool:
        stmt = insert(InboxModel).values(event_id = inbox.eventID).on_conflict_do_nothing()
        result : CursorResult  = await self._session.execute(stmt)

        return result.rowcount == 1