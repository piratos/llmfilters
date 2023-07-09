from llmfilters.blocks.manager import BlockManager

class BaseManager:
    type = 'base'
    
    def __init__(self, config, config_file):
        self.config = config
        self.config_file = config_file
        self.block_manager = None

    def load_pipeline(self):
        self.block_manager = BlockManager(self.config_file)

    def connect(self):
        pass

    def start_consuming(self):
        pass

    def process_event(self, event):
        pass

    def run(self):
        self.load_pipeline()
        self.connect()
        self.start_consuming()
