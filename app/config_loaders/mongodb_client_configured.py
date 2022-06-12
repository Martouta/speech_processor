import os
from pathlib import Path
import pymongo
import yaml
from mako.template import Template


def mongodb_client_configured():
    '''
    It returns the Mongo Client, the database and the collection.
    It fetches the customizable info from the config file, according to the env
    (which is assumed present)
    '''

    speech_env = os.environ['SPEECH_ENV']
    path_mongodb_yml = f"{Path(__file__).resolve().parent.parent.parent}/config/mongodb.yml.mako"

    config = {}

    with open(path_mongodb_yml, 'r') as file:
        text = file.read()
        template_rendered = Template(text).render()
        config = yaml.load(template_rendered, yaml.Loader)[speech_env]

    mongo_uri = f"mongodb://{config['host_with_port']}/"
    client = pymongo.MongoClient(mongo_uri)
    database = client[config['database']]

    return {
        'client': client,
        'database': database,
        'collection': database['subtitles']
    }
