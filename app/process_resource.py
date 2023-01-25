import logging
import traceback

from .cleanup_temporary_files import cleanup_temporary_files
from .models.resource_audio import ResourceAudio
from .converters.resource_json_to_input_item import resource_json_to_input_item
from .converters.resource_message_to_json import resource_message_to_json


def process_resource(msg):
    """
    Processes a resource message.
    It converts the message to json, converts the json to a input_item, saves the input_item,
    converts the input_item to audio, splits the audio into chunks, recognizes the chunks and
    saves the recognition results in the mongodb.
    :param msg: The message to process, it should contain a json with the resource information.
    :return: A json with the status of the processing, the recognition_id and the location of the subtitles.
    """
    try:
        json = resource_message_to_json(msg)
        input_item = resource_json_to_input_item(json)
        return __process_resource(input_item)
    except Exception as exc:
        message = __error_msg((type(exc), exc, traceback.format_exc()))
        logging.getLogger(__name__).error(message)
        return {'status': 'error', 'error': exc}


def __process_resource(input_item):
    log_step(0, input_item.recognition_id)
    filepath = input_item.save()
    log_step(1, input_item.recognition_id)
    audio = ResourceAudio.save_as_wav(input_item.recognition_id, filepath)
    log_step(2, input_item.recognition_id)
    audio.split_into_chunks()
    log_step(3, input_item.recognition_id)
    subtitle = audio.recognize_all_chunks(input_item.language_code)
    log_step(4, input_item.recognition_id)
    subs_location = subtitle.save_subs(input_item.resource_id)
    log_step(5, input_item.recognition_id)
    cleanup_temporary_files(input_item.recognition_id, filepath)
    log_step(6, input_item.recognition_id)
    response = {
        'status': 'ok',
        'input_item.recognition_id': input_item.recognition_id,
    }
    return {**response, **subs_location}


def log_step(step_number, recognition_id):
    """
    Logs the current step of the processing.
    :param step_number: The number of the step.
    :param recognition_id: The recognition_id to add to the log.
    """
    total_steps = 6
    steps = [
        f"[1/{total_steps}] Downloading multimedia from URL ... [{recognition_id}]",
        f"[2/{total_steps}] Saving audio as WAP ... [{recognition_id}]",
        f"[3/{total_steps}] Spliting into chunks ... [{recognition_id}]",
        f"[4/{total_steps}] Recognizing chunks ... [{recognition_id}]",
        f"[5/{total_steps}] Saving subtitles ... [{recognition_id}]",
        f"[6/{total_steps}] Cleaning up temporary generated files ... [{recognition_id}]",
        f"[DONE] [{recognition_id}]"
    ]
    logging.info(steps[step_number])


def __error_msg(exc_tuple):
    text = """{type} : {value}
    TRACEBACK:
    {tb}"""
    return text.format(
        type=exc_tuple[0],
        value=exc_tuple[1],
        tb=exc_tuple[2]).strip()
