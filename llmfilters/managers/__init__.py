import importlib
from llmfilters.managers.simple_manager import SimpleManager

__all__ = [
    'SimpleManager',
]

try:
    import pika
    from llmfilters.managers.rabbitmq_manager import RabbitMQManager
    __all__.append('RabbitMQManager')
except ImportError:
    pass

try:
    import kafka
    from llmfilters.managers.kafka_manager import KafkaManager
    __all__.append('KafkaManager')
except ImportError:
    pass


def get_manager(manager_type):
    managers = {}
    module = module = importlib.import_module('llmfilters.managers')
    for manager_name in __all__:
        manager = getattr(module, manager_name)
        managers[manager.type] = manager
    
    print(f'Imported managers {managers}')
    
    if manager_type in managers:
        return managers[manager_type]
    else:
        raise Exception(f'Cannot find Manager of type {manager_type}')