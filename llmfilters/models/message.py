class Message:
    def __init__(self, text, metadata=None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}
        self.passed_by = []
        self.changed_by = []
        self.refused_by = []

    def to_dict(self):
        return {
            'text': self.text,
            'metadata': self.metadata,
            'passed_by': self.passed_by,
            'refused_by': self.refused_by,
            'changed_by': self.changed_by,
        }
    
    def passed(self, block_name):
        self.passed_by.append(block_name)
    
    def changed(self, block_name):
        self.changed_by.append(block_name)

    def refused(self, block_name):
        self.refused_by.append(block_name)
    

    @classmethod
    def from_dict(cls, data):
        return cls(data['text'], data['metadata'])
    
    def __repr__(self) -> str:
        return str(self.to_dict())