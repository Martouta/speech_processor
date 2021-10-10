from datetime import datetime
import logging
import os
import traceback
import threading

from .cleanup_temporary_files import cleanup_temporary_files
from .download_multimedia_from_url import download_multimedia_from_url
from .resource_audio import ResourceAudio


def process_resource(json_parsed):
    try:
        return __process_resource(json_parsed)
    except Exception as exc:
        message = __error_msg((type(exc), exc, traceback.format_exc()))
        if os.environ['SPEECH_ENV'] != 'test':
            logging.error(message)
        return {'status': 'error', 'error': exc}


def __process_resource(json_parsed):
    thread_id = threading.get_ident()
    datetime_now = datetime.utcnow().strftime('%m-%d.%H:%M:%S%f')
    recognition_id = f"{thread_id}-{json_parsed['id']}-{datetime_now}"
    total_steps = '6'
    logging.info(
        '[1/%s] Downloading multimedia from URL ... [%s]', total_steps, recognition_id)
    filepath = download_multimedia_from_url(recognition_id, json_parsed)
    logging.info(
        '[2/%s] Saving audio as WAP ... [%s]', total_steps, recognition_id)
    resource_audio = ResourceAudio.save_as_wav(recognition_id, filepath)
    logging.info(
        '[3/%s] Spliting into chunks ... [%s]', total_steps, recognition_id)
    resource_audio.split_into_chunks()
    logging.info(
        '[4/%s] Recognizing chunks ... [%s]', total_steps, recognition_id)
    subtitle = resource_audio.recognize_chunks(json_parsed['language_code'])
    logging.info(
        '[5/%s] Saving subtitles ... [%s]', total_steps, recognition_id)
    subs_location = subtitle.save_subs(json_parsed['id'])
    logging.info(
        '[6/%s] Cleaning up temporary generated files ... [%s]', total_steps, recognition_id)
    cleanup_temporary_files(recognition_id, filepath)
    logging.info('[DONE] [%s]', recognition_id)
    response = {
        'status': 'ok',
        'recognition_id': recognition_id,
    }
    return {**response, **subs_location}


def __error_msg(exc_tuple):
    text = """{type} : {value}
    TRACEBACK:
    {tb}"""
    return text.format(
        type=exc_tuple[0],
        value=exc_tuple[1],
        tb=exc_tuple[2]).strip()
