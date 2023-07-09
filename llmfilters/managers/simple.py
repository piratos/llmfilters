import asyncio

from llmfilters.blocks.manager import BlockManager
from llmfilters.managers.base import BaseManager

class SimpleManager(BaseManager):
    type = 'simple'

    def __init__(self, config, config_file):
        self.config_file = config_file
        self.block_manager = None

    def load_pipeline(self):
        self.block_manager = BlockManager(self.config_file)

    async def run_pipeline(self, input_text):
        return await self.block_manager.process_input(input_text)

    async def process_input(self, input_text):
        output = await self.run_pipeline(input_text)
        return output

    async def run(self):
        self.load_pipeline()

        while True:
            input_text = input("Enter input text (or 'exit' to quit): ")
            if input_text == "exit":
                break

            output = await self.process_input(input_text)
            print("Output:", output)
