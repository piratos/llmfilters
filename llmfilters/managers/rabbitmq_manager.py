import pika
import json
import uuid

from llmfilters.managers.base import BaseManager

class RabbitMQManager(BaseManager):
    type = 'rabbitmq'

    def __init__(self, config, config_file):
        self.config = config
        self.config_file = config_file
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

    def start_consuming(self):
        self.channel.basic_consume(queue=self.config['input_queue'], on_message_callback=self.process_event, auto_ack=True)
        self.channel.start_consuming()

    def process_event(self, channel, method, properties, body):
        event = json.loads(body)
        input_text = event['text']
        event_id = event['id']

        # Call BlockManager for processing
        output = self.block_manager.process_input(input_text)

        # Create a new event with a link to the input event
        result_event = {
            'id': str(uuid.uuid4()),  # Generate a unique identifier for the output event
            'input_id': event_id,  # Link the output event to the input event
            'output': output
        }
        self.channel.basic_publish(exchange='', routing_key=self.config['output_queue'], body=json.dumps(result_event))

    def run(self):
        self.load_pipeline()
        self.connect()
        self.setup_queues()
        self.start_consuming()