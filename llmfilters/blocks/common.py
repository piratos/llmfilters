from llmfilters.blocks.base import FilterBlock

class EntryFilterBlock(FilterBlock):
    def __init__(self, config, next_block=None):
        super().__init__(config, next_block)

    def process_input(self, messsage):
        return super().process_input(messsage)


class ExitFilterBlock(FilterBlock):
    def __init__(self, config, next_block=None):
        super().__init__(config, next_block)

    def apply_changes(self, messsage):
        modified_input = super().apply_changes(messsage)
        return modified_input

class LengthFilterBlock(FilterBlock):
    def __init__(self, params, next_block=None):
        super().__init__(params, next_block)
        self.max_length = params.get('max_length', None)

    def apply_changes(self, message):
        if self.max_length is not None and len(message.text) > self.max_length:
            message.text = message.text[:self.max_length]
            message.changed(self.__class__.__name__)
        return message