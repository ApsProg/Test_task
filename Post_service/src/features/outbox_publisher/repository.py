from uuid import  UUID

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from models import OutboxModel

class OutboxRepository:

    def __init__(self, session: AsyncSession):
        self._session = session
    async def save_outbox(self, outbox: OutboxModel) -> None:
        self._session.add(outbox)

    async def get_unpublished(self) -> OutboxModel:

        res = await self._session.execute(select(OutboxModel).where(OutboxModel.status == "unpublished"))

        unpublished = res.scalars().all()

        if not unpublished:
            return None
        else:
            return unpublished
    async def chande_published(self, id: UUID) -> None:
        await self._session.execute(update(OutboxModel).where(OutboxModel.uuid == id))
        await self._session.commit()
