from setuptools import setup, find_packages

setup(
    name='llmfilters',
    version='0.1.0',
    author='piratos',
    description='LLM Filters Package',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
    ],
    extras_require={
        'rabbitmq': ['pika'],  # Additional requirement for RabbitMQ integration
        'kafka': ['kafka-python'],  # Additional requirement for Kafka integration
    },
    entry_points={
        'console_scripts': [
            'llmfilters-run-pipeline = llmfilters.run_pipeline:main',
        ],
    },
)