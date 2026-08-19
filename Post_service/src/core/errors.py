from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.features.callbacks.exceptions import CallbackNotFound, InvalidPhoneNumber


def register_exception_handler(app: FastAPI):
    @app.exception_handler(CallbackNotFound)
    async def callback_not_found(_: Request, exc: CallbackNotFound) -> JSONResponse:
        return JSONResponse(status_code = 404, content = {"error": "callback_not_found", "callback_id":  str(exc.callback_id)},)

    @app.exception_handler(InvalidPhoneNumber)
    async def invalid_phone(_: Request, exc: InvalidPhoneNumber) -> JSONResponse:
        return JSONResponse(status_code = 422, content = {"error": "invalid_phone", "phone": str(exc)},)
