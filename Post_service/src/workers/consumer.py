import asyncio
from aiokafka import AIOKafkaConsumer

from src.features.consume_responce.kafka_repo import  KafkaConsumer
from src.features.consume_responce.service import Consumer_service
from src.core.confog import settings
from src.core.uow import UnitOfWork


async def main():
    consumer = KafkaConsumer()
    uow = UnitOfWork()

    service = Consumer_service(uow= uow, consumer = consumer)

    await service.consumer_service()

if __name__ == "__main__":
    asyncio.run(main())

