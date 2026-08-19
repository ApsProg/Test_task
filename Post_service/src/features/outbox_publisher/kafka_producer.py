from aiokafka import AIOKafkaProducer
import asyncio
from shemas import outbox_product
class KafkaProducer:
    def __init__(self, producer : AIOKafkaProducer , topic : str ):
        self._producer = producer
        self._topic = topic
    async def start(self) -> None:
            await self._producer.start()
    async def send_event(self, event: outbox_product) -> None:
        payload = event.model_dump_json().encode("utf-8")
        await self._producer.send_and_wait(self._topic, payload)
    async def close(self) -> None:
        await self._producer.stop()
