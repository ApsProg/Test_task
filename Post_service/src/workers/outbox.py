import asyncio
from aiokafka import AIOKafkaProducer

from src.features.outbox_publisher.kafka_producer import  KafkaProducer
from src.features.outbox_publisher.service import OutboxPublisherService
from src.core.confog import settings
from src.core.uow import UnitOfWork
async def main():
    producer = KafkaProducer()
    uow = UnitOfWork()

    service = OutboxPublisherService(uow = uow, kafka_producer= producer)

    await service.outbox_publisher()

if __name__ == "__main__":
    asyncio.run(main())

