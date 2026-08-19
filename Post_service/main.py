import asyncio
from pydoc_data.topics import topics

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from fastapi import FastAPI


from src.core.confog import settings
from src.core.errors import register_exception_handler
from src.core.logging import register_logger
from src.features.callbacks.router import api as callback_router

# middleware ?


def create_app() -> FastAPI:
    register_logger()
    app = FastAPI(title = settings.service_name)
    register_exception_handler(app)
    app.include_router(callback_router)
    return app
app = create_app()