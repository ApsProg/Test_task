from aiokafka import AIOKafkaConsumer
from kafka_event_shema import kafka_event

class KafkaConsumer:
    def __init__(self, consumer: AIOKafkaConsumer) -> None:
        self._consumer = consumer

    async def start(self) -> None:
        await self._consuer.start()

    async def consume_msgs(self) -> kafka_event:
        try:
            messages = []
            for msg in self._consumer:
                messages.append(kafka_event(msg.value()).model_validate_json())
            return messages
        except Exception as e:
            raise e
    async def stop(self) -> None:
        await self._consumer.stop()
