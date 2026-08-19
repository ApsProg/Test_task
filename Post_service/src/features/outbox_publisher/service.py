
import structlog
from aiokafka.errors import KafkaError

from sqlalchemy.ext.asyncio import AsyncSession
from structlog import logger
from asyncio import sleep

from kafka_producer import KafkaProducer
from shemas import outbox_product
from repository import OutboxRepository
from src.core.uow import UnitOfWork

logger = structlog.get_logger(__name__)

class OutboxPublisherService:

    def __init__(self, uow: UnitOfWork, kafka_producer: KafkaProducer) -> None:
        self._uow = uow
        self._producer = kafka_producer

    async def outbox_publisher(self) -> None:

        await self._producer.start()

        try:
            while True:
                try:

                    unpublished_msgs = self._uow.outbox.get_unpublished()
                    if not unpublished_msgs:
                        await sleep(15)
                        continue
                    for msg in unpublished_msgs:
                        payload = {}
                        payload["name"] = msg.name
                        payload["phone"] = msg.phone_number
                        payload["source"] = msg.source
                        payload["comment"] = msg.comment

                        event = outbox_product(event_id = msg.event_id, ocuured_at = msg.occured_at, event = msg.event , payload = payload)
                        await self._poducer.publish(event)
                        await sleep(5)
                except KafkaError:
                    logger.exception("Kafka error")
                    await sleep(15)

                except Exception:
                    logger.exception("Unexpected publisher error")
                    await sleep(15)
        finally:
            await self._producer.stop()
