from _collections_abc import Callable

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import async_session_factory
from src.features.outbox_publisher.repository import  OutboxRepository
from src.features.callbacks.repository import CallbackRepository
from src.features.consume_responce.repository import  InboxRepository

class UnitOfWork:

    callbacks: CallbackRepository
    outbox: OutboxRepository
    inbox : InboxRepository
    def __init__(self, session_factory: Callable[[], AsyncSession] = async_session_factory)->None:
        self._session_factory = session_factory

    async def __aenter__(self)-> UnitOfWork:
        self._session = self._session_factory()
        self.callbacks = CallbackRepository(self._session)
        self.outbox = OutboxRepository(self._session)
        return self
    async def __aexit__(self, exc_type: type(BaseException) | None , exc_val: BaseException | None, exc: TracebackType | None)-> None:
        if exc_type is not None:
            await self._session.rollback()
        self._session.close()

    async def commit(self) -> None:
        await self._session.commit()
    async def rollback(self):
        await sekf._session.rollback()


