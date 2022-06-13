from datetime import datetime
import logging
import os
import traceback
import threading

from .cleanup_temporary_files import cleanup_temporary_files
from .downloaders.download_multimedia import download_multimedia
from .models.resource_audio import ResourceAudio


def process_resource(json_parsed):
    try:
        recognition_id = generate_recognition_id(json_parsed)
        return __process_resource(json_parsed, recognition_id)
    except Exception as exc:
        message = __error_msg((type(exc), exc, traceback.format_exc()))
        if os.environ['SPEECH_ENV'] != 'test':
            logging.error(message)
        return {'status': 'error', 'error': exc}


def __process_resource(json_parsed, recognition_id):
    log_step(0, recognition_id)
    filepath = download_multimedia(recognition_id, json_parsed)
    log_step(1, recognition_id)
    resource_audio = ResourceAudio.save_as_wav(recognition_id, filepath)
    log_step(2, recognition_id)
    resource_audio.split_into_chunks()
    log_step(3, recognition_id)
    subtitle = resource_audio.recognize_chunks(json_parsed['language_code'])
    log_step(4, recognition_id)
    resource_id = int(json_parsed['resource_id'] or -1)
    subs_location = subtitle.save_subs(resource_id)
    log_step(5, recognition_id)
    cleanup_temporary_files(recognition_id, filepath)
    log_step(6, recognition_id)
    response = {
        'status': 'ok',
        'recognition_id': recognition_id,
    }
    return {**response, **subs_location}


def generate_recognition_id(json_parsed):
    thread_id = threading.get_ident()
    datetime_now = datetime.utcnow().strftime('%m-%d.%H:%M:%S%f')
    resource_id = int(json_parsed['resource_id'] or -1)
    return f"{thread_id}-{resource_id}-{datetime_now}"


def log_step(step_number, recognition_id):
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
