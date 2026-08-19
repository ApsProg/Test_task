from aiokafka.errors import KafkaError

from kafka_repo import KafkaConsumer
from repository import InboxModel
from kafka_event_shema import kafka_event
from src.core.uow import  UnitOfWork
import asyncio
from structlog import get_logger

from time import sleep

logger = get_logger(__name__)

class Consumer_service:
    def __init__(self, consumer: KafkaConsumer, uow : UnitOfWork):
        self._consumer = consumer
        self._uow = uow
    async def consumer_service(self) -> None:
        try:
            while True:
                try:
                    kafka_events = await self._consumer.consume_msgs()
                    if not kafka_events:
                        sleep(15)
                        continue
                    for kafka_event in kafka_events:
                        with self._uow as uow:
                            is_new = await uow.inbox.add_if_new(kafka_event)
                            if is_new:
                                status = kafka_event.payload["approved"]
                                lead_id = kafka_event.payload["lead_id"]
                                if status:
                                    await uow.callbacks.change_status(lead_id, "approved")
                                else:
                                    await uow.callbacks.change_status(lead_id, "rejected")
                                await uow.commit()
                except KafkaError:
                    logger.exception("Kafka error")
                    await asyncio.sleep(15)

                except Exception:
                    logger.exception("Unexpected consumer error")
                    await asyncio.sleep(15)
            sleep(5)
        finally:
            self._consumer.close()
