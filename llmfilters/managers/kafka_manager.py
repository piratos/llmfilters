from kafka import KafkaConsumer, KafkaProducer
import json
import uuid

from llmfilters.managers.base import BaseManager

class KafkaManager(BaseManager):
    type = 'kafka'

    def __init__(self, config, config_file):
        self.config = config
        self.config_file = config_file
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

    def start_consuming(self):
        for message in self.consumer:
            event = message.value
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
            self.producer.send(self.config['output_topic'], value=result_event)

    def run(self):
        self.load_pipeline()
        self.connect()
        self.start_consuming()