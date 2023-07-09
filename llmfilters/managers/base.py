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

    async def start_consuming(self):
        pass

    async def process_event(self, event):
        pass

    async def run(self):
        self.load_pipeline()
        self.connect()
        await self.start_consuming()
