import os
from pathlib import Path
import yaml
from mako.template import Template


def tiktok_cookie_configured():
    '''
    It returns the tiktok cookie data.
    It fetches the info from the config file, according to the env
    (which is assumed present)
    '''

    speech_env = os.environ['SPEECH_ENV']
    path_yml = f"{Path(__file__).resolve().parent.parent}/config/tiktok_cookie.yml.mako"

    config = {}

    with open(path_yml, 'r') as file:
        text = file.read()
        template_rendered = Template(text).render()
        config = yaml.load(template_rendered, yaml.Loader)[speech_env]

    return {
        's_v_web_id': config['s_v_web_id'],
        'tt_webid': config['tt_webid']
    }
