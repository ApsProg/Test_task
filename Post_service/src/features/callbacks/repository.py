from uuid import  UUID

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from src.features.callbacks.exceptions import CallbackNotFound


from models import *

class CallbackRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, callback: CallbackModel) -> None:
        self._session.add(callback)

    async def find(self, event_id: UUID) -> CallbackModel:
        res = await self._session.execute(select(CallbackModel).where(CallbackModel.id == event_id))

        callback = res.fetchone()\

        if callback is None:
            raise CallbackNotFound(event_id)
        return callback
    async def change_status(self, callback_id: UUID, status : str) -> None:
        await self._session.execute(update(CallbackModel).where(CallbackModel.id == callback_id).values(status = status))
