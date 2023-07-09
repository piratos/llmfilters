import importlib
from llmfilters.managers.simple import SimpleManager

__all__ = [
    'SimpleManager',
]

try:
    import pika
    from llmfilters.managers.rabbitmq import RabbitMQManager
    __all__.append('RabbitMQManager')
except ImportError:
    pass

try:
    import kafka
    from llmfilters.managers.kafka import KafkaManager
    __all__.append('KafkaManager')
except ImportError:
    raise
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