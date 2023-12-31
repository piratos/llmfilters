class FilterBlock:
    def __init__(self, config, next_block=None):
        self.config = config
        self.next_block = next_block
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}-<{self.next_block.__class__.__name__}>'

    def apply_changes(self, message):
        # Apply changes to the input text based on the filter's configuration
        # Modify the input as needed and return the modified text
        message.passed(self.__class__.__name__)
        return message

    def refuse_input(self, message):
        # Determine if the input should be refused based on the filter's configuration
        # Return True to refuse the input, False otherwise
        pass

    def process_input(self, message):
        print(f'{self.__class__.__name__} - Processing {message}')
        if self.refuse_input(message):
            self.handle_refused_input(message)
        else:
            modified_message = self.apply_changes(message)
            if self.next_block is not None:
                return self.next_block.process_input(modified_message)
            else:
                return message

    def handle_refused_input(self, input_text):
        # Handle the refused input, e.g., generate an automated response to inform the user
        pass
