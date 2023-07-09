from llmfilters.blocks.base import FilterBlock

class ProfanityFilterBlock(FilterBlock):
    def __init__(self, params, next_block=None):
        super().__init__(params, next_block=next_block)
        self.profanity_words = params.get('profanity_words', [])

    def apply_changes(self, message):
        for word in self.profanity_words:
            message.text = message.text.replace(word, '[FILTERED]')
        if '[FILTERED]' in message.text:
            message.changed(self.__class__.__name__)
        return message