import logging
import os
from pathlib import Path
import yaml
from kafka import KafkaConsumer
from mako.template import Template


def kafka_consumer_configured():
    '''
    It assumes correct config file.
    It also assumes the correct SPEECH_ENV set.
    It loads the YAML file and returns a kafka consumer configured accordingly.
    '''
    speech_env = os.environ['SPEECH_ENV']
    path_kafka_yml = f"{Path(__file__).resolve().parent.parent.parent}/config/kafka.yml.mako"
    with open(path_kafka_yml, 'r') as file:
        text = file.read()
        template_rendered = Template(text).render()
        config = yaml.load(template_rendered, yaml.Loader)[speech_env]
        if speech_env != 'test': # Because I rather to be able to run all tests without kafka running and just see it fail instead of hanging
            logging.info('Waiting for the kafka server to be reachable (not necessarily ready)')
            os.system(f"while ! nc -zv {config['brokers'].replace(':', ' ')} -w 5; do sleep 20; done")
        consumer = KafkaConsumer(config['topic_publish_resource'],
                             bootstrap_servers=config['brokers'],
                             group_id='1'
                             )
        logging.info('Connection to kafka established')
        return consumer
