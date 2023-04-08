import logging
import traceback
from app.services.resource_processors.ai_resource_processor import AiResourceProcessor
from app.services.resource_processors.captions_resource_processor import CaptionsResourceProcessor
from .converters.resource_json_to_input_item import resource_json_to_input_item
from .converters.resource_message_to_json import resource_message_to_json


def process_resource(msg):
    try:
        json = resource_message_to_json(msg)
        input_item = resource_json_to_input_item(json)
        return input_item.call_resource_processor()
    except Exception as exc:
        message = __error_msg((type(exc), exc, traceback.format_exc()))
        logging.getLogger(__name__).error(message)
        return {'status': 'error', 'error': exc}


def __error_msg(exc_tuple):
    text = """{type} : {value}
    TRACEBACK:
    {tb}"""
    return text.format(
        type=exc_tuple[0],
        value=exc_tuple[1],
        tb=exc_tuple[2]).strip()
