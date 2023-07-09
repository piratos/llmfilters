from kafka import KafkaConsumer, KafkaProducer
import json
import asyncio
import uuid

from llmfilters.blocks.manager import BlockManager
from llmfilters.managers.base import BaseManager

class KafkaManager(BaseManager):
    type = 'kafka'

    def __init__(self, config):
        self.config = config
        self.consumer = None
        self.producer = None
        self.block_manager = None

    def connect(self):
        self.consumer = KafkaConsumer(
            self.config['input_topic'],
            bootstrap_servers=self.config['bootstrap_servers'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            group_id=self.config['group_id']
        )
        self.producer = KafkaProducer(
            bootstrap_servers=self.config['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    async def start_consuming(self):
        for message in self.consumer:
            event = message.value
            input_text = event['text']
            event_id = event['id']

            # Call BlockManager for processing
            output = await self.block_manager.process_input(input_text)

            # Create a new event with a link to the input event
            result_event = {
                'id': str(uuid.uuid4()),  # Generate a unique identifier for the output event
                'input_id': event_id,  # Link the output event to the input event
                'output': output
            }
            self.producer.send(self.config['output_topic'], value=result_event)

    async def run(self):
        self.connect()
        await self.start_consuming()

    async def run(self):
        config = {
            'bootstrap_servers': self.config.get('bootstrap_servers', 'localhost:9092'),
            'input_topic': self.config.get('input_topic', 'input_topic'),
            'output_topic': self.config.get('output_topic', 'output_topic'),
            'group_id': self.config.get('group_id', 'my-group')
        }

        manager = KafkaManager(config)
        block_manager = BlockManager()
        manager.block_manager = block_manager
        await manager.run()
