import os
from .json_input_resources import json_input_resources
from .config_loaders.kafka_consumer_configured import kafka_consumer_configured


def fetch_input_messages():
    input_file = os.getenv('INPUT_FILE')
    if input_file:
        return json_input_resources(input_file)
    else:
        return kafka_consumer_configured()
