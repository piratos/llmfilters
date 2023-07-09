from llmfilters.blocks.base import FilterBlock
from transformers import pipeline

class SentimentAnalysisFilterBlock(FilterBlock):
    def __init__(self, params, next_block=None):
        super().__init__(params, next_block=next_block)
        if 'model_name' in params:
            self.sentiment_analyzer = pipeline("sentiment-analysis", model=params['model_name'])
        else:
            self.sentiment_analyzer = pipeline("sentiment-analysis")

    def apply_changes(self, message):
        results = self.sentiment_analyzer(message.text)
        sentiment = results[0]["label"]
        message.metadata['sentiment'] = sentiment
        return message
