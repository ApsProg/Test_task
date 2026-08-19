from datetime import UTC, datetime
from uuid import UUID

import structlog

from src.core.uow import  UnitOfWork
from src.features.callbacks.models import  CallbackModel
from src.features.callbacks.events import CallbackRequested
from src.features.callbacks.schemas import CallbackRequest

logger = structlog.get_logger(__name__)

class CallbackService:

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def create_callback(self, request: CallbackRequest)->CallbackModel:
        with self._uow as uow:
            callback = CallbackModel(phone_number = request.phone, name = request.name)
            await uow.callbacks.save(callback)
            event = CallbackRequested(event = "lead_created.v1",name = request.name, phone_number = request.phone, source = request.source, comment = request.comment)
            await uow.outbox.save(event)
        logger.info("Created callback.v1", callback_id = callback.id, phone = callback.phone_number)
        return callback
    async def find_callback(self, callback_id: UUID) -> CallbackModel:
        with self._uow as uow:
            return await uow.callbacks.find_by_id(callback_id)
