from llmfilters.blocks.filter_block import FilterBlock
from transformers import pipeline

class SentimentAnalysisFilterBlock(FilterBlock):
    def __init__(self, params):
        super().__init__(params)
        self.sentiment_analyzer = pipeline("sentiment-analysis")

    def apply_changes(self, message):
        results = self.sentiment_analyzer(message.text)
        sentiment = results[0]["label"]
        message.metadata['sentiment'] = sentiment
        return text
