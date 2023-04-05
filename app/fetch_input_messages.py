import logging
import os
import json
from .config_loaders.kafka_consumer_configured import kafka_consumer_configured


def fetch_input_messages():
    logging.getLogger(__name__).info('Fetching input messages')
    filepath = os.getenv('INPUT_FILE')
    if filepath:
        with open(filepath, 'r') as file:
            text = file.read()
            return json.loads(text)
    else:
        return kafka_consumer_configured()
