import importlib
import yaml

from llmfilters.models.message import Message

class BlockManager:
    def __init__(self, config_file):
        self.blocks = []
        self.load_pipeline(config_file)
        print(f'Block manager loaded {self.blocks}')

    def load_pipeline(self, config_file):
        with open(config_file, 'r') as file:
            pipeline_config = yaml.safe_load(file)

        for i, block_config in enumerate(reversed(pipeline_config['blocks'])):
            block_type = block_config['type']
            block_params = block_config.get('params', {})
            next_block = self.blocks[-1] if i > 0 else None
            block = self.create_block(block_type, block_params, next_block=next_block)
            self.blocks.append(block)
        self.blocks = list(reversed(self.blocks))

    def create_block(self, block_type, block_params, next_block=None):
        module_name, class_name = block_type.rsplit('.', 1)
        try:
            module = importlib.import_module(module_name)
            block_class = getattr(module, class_name)
            return block_class(block_params, next_block=next_block)
        except (ImportError, AttributeError) as e:
            raise ValueError(f"Failed to create block {block_type}: {str(e)}")

    def process_input(self, input_text):
        new_message = Message(input_text)
        output_message = self.blocks[0].process_input(new_message)
        return output_message.text