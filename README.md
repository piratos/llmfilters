# LLM Filters

LLM Filters is a project that demonstrates the use of language models (LLMs) to create a pipeline for processing and filtering text data. It provides a framework for building custom filters using LLMs, and includes managers for integrating with messaging systems such as RabbitMQ and Kafka.

## Project Structure

The project structure is as follows:

llmfilters/
|- init.py
|- blocks/
| |- init.py
| |- filter_block.py
|- managers/
| |- init.py
| |- rabbitmq.py
| |- kafka.py
|- pipeline.yaml


- `llmfilters/` is the main package directory.
- `blocks/` directory contains the custom filter blocks implemented using LLMs.
- `managers/` directory contains the managers for integrating with RabbitMQ and Kafka messaging systems.
- `pipeline.yaml` is the YAML configuration file that defines the pipeline structure.

## Blocks

The following custom filter blocks are available:

### FilterBlock

The `FilterBlock` is a base class for creating custom filters. It provides methods for applying changes, refusing input, and handling refused input.

To create a custom filter block, you can inherit from the `FilterBlock` class and implement the required methods.

## Managers

The following managers are provided for integrating with messaging systems:

### RabbitMQManager

The `RabbitMQManager` allows processing text data using the LLM pipeline with RabbitMQ as the messaging system. It connects to a RabbitMQ server, consumes input events, processes them through the pipeline, and produces output events.

### KafkaManager

The `KafkaManager` allows processing text data using the LLM pipeline with Kafka as the messaging system. It connects to a Kafka broker, consumes input events, processes them through the pipeline, and produces output events.

### Example with simple manager

Simple manager is useful to test the pipeline rather than using it in production

```
import asyncio
from llmfilters.managers import SimpleManager

async def run_manager():
    config_file = "pipeline.yaml"

    manager = SimpleManager(config_file)
    block_manager = BlockManager()
    manager.block_manager = block_manager

    await manager.run()

if __name__ == '__main__':
    asyncio.run(run_manager())
```

## Pipeline Configuration

The pipeline configuration is defined in the `pipeline.yaml` file. It specifies the sequence of filter blocks to be applied in the pipeline. Each block is defined with its type and parameters.

Example `pipeline.yaml` configuration:

```yaml
- type: llmfilters.blocks.filter_block.FilterBlock
  params:
    param1: value1
    param2: value2
- type: llmfilters.blocks.filter_block.FilterBlock
  params:
    param1: value3
    param2: value4
```

In this example, two FilterBlock instances are defined in the pipeline. Each block can have specific parameters based on the requirements.

Feel free to update the README.md file with additional details specific to your project, such as installation instructions, usage examples, and any additional blocks or managers you may have implemented.

Remember to update the directory structure and details based on your specific implementation.

Happy filtering!