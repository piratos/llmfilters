import pika
import json
import asyncio
import uuid

from llmfilters.blocks.manager import BlockManager
from llmfilters.managers.base import BaseManager

class RabbitMQManager(BaseManager):
    type = 'rabbitmq'

    def __init__(self, config):
        self.config = config
        self.connection = None
        self.channel = None
        self.block_manager = None

    def connect(self):
        credentials = pika.PlainCredentials(self.config['username'], self.config['password'])
        parameters = pika.ConnectionParameters(self.config['host'], self.config['port'], self.config['virtual_host'], credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def setup_queues(self):
        self.channel.queue_declare(queue=self.config['input_queue'], durable=True)
        self.channel.queue_declare(queue=self.config['output_queue'], durable=True)

    async def start_consuming(self):
        self.channel.basic_consume(queue=self.config['input_queue'], on_message_callback=self.process_event, auto_ack=True)
        self.channel.start_consuming()

    async def process_event(self, channel, method, properties, body):
        event = json.loads(body)
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
        self.channel.basic_publish(exchange='', routing_key=self.config['output_queue'], body=json.dumps(result_event))

    async def run(self):
        self.connect()
        self.setup_queues()
        await self.start_consuming()

    async def run(self):
        config = {
            'host': self.config.get('host', 'localhost'),
            'port': self.config.get('port', 5672),
            'virtual_host': self.config.get('virtual_host', '/'),
            'username': self.config.get('username', 'guest'),
            'password': self.config.get('password', 'guest'),
            'input_queue': self.config.get('input_queue', 'input_queue'),
            'output_queue': self.config.get('output_queue', 'output_queue')
        }

        manager = RabbitMQManager(config)
        block_manager = BlockManager()
        manager.block_manager = block_manager

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, manager.run)