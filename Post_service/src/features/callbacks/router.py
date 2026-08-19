from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.features.callbacks.schemas import  CallbackRequest, CallbackResponse
from src.features.callbacks.service import CallbackService
from src.features.callbacks.deps import get_callback_service
api = APIRouter(prefix = "/callbacks", tags = ["callbacks"])


@api.post("", response_model = CallbackResponse, status_code = status.HTTP_201_CREATED)
async def post_callback(request: CallbackRequest, service: CallbackService = Depends(get_callback_service)) ->CallbackResponse:
    callback = await service.create_callback(request)

    return CallbackResponse(id = callback.id, phone = callback.phone_number, status = callback.status, created_at = callback.created_at)

@api.get("/{callback_id}", response_model = CallbackResponse)
async def get_callback(uuid: UUID, service: CallbackService = Depends(get_callback_service)) ->CallbackResponse:
    callback = await service.find_callback(uuid)

    return CallbackResponse(id = callback.id, phone = callback.phone_number, status = callback.status, created_at = callback.created_at)
