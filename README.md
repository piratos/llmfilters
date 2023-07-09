# LLM Filters

<img src="https://github.com/piratos/llmfilters/blob/main/llmfilters/assets/logo.png" width="600" height="500">

LLM Filters is a pipeline library for processing and filtering text data that go in and out from LLM engines. It provides a framework for building custom filters, and includes managers for integrating with messaging systems such as RabbitMQ and Kafka.

When building an LLM based app, you want to control data going into the model, like the length, profanity removal, fact checking etc.
and you want to control data out, to verify whether the LLM is hallucinating, fact checking etc.

the building blocks are Filterblocks, the message is passed through a set of filterblocks and each one of them has a couple of possible actions:

- Modify the message (like removing profanity)
- Passing the message to the next block (with or without modifying it)
- Halting the pipeline and preventing the message to go to the LLM
- Adding metadata to the message, which can be used by other filterblocks or can be used to prepare the final prompt going to the user
  or to the LLM.

## Project Structure

The project structure is as follows:


- `llmfilters/` is the main package directory.
- `blocks/` directory contains the custom filter blocks implemented.
- `managers/` directory contains the managers for integrating with RabbitMQ and Kafka messaging systems.
- `models` directory contains the objects structure used by the filters, mainly the message format.
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
manager:
  type: simple

blocks:
- type: llmfilters.blocks.FilterBlock1
  params:
    param1: value1
    param2: value2
- type: llmfilters.blocks.FilterBlock2
  params:
    param1: value3
    param2: value4
```

In this example, two FilterBlock instances are defined in the pipeline. Each block can have specific parameters based on the requirements.
See `examples` folder for examples of piplines

The manager entry exposes the type and configuration of the manager handling the events

Happy filtering!
