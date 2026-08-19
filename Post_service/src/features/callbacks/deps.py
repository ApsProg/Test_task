from fastapi import Depends

from src.core.uow import UnitOfWork
from src.features.callbacks.service import CallbackService

def get_uow() -> UnitOfWork:
    return UnitOfWork()

def get_callback_service(uow: UnitOfWork = Depends(get_uow)) -> CallbackService:
    return CallbackService(uow = uow)

