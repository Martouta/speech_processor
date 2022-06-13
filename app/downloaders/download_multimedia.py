import os
from pathlib import Path
import requests
from .download_tiktok_video import download_tiktok_video
from .download_youtube_video import download_youtube_video


def download_multimedia(recognition_id, json_parsed):
    '''
    Download video or audio from URL and returns the path where it has been saved.
    If there is a video, it downloads it, otherwise, it goes for the audio.
    It assumes that at least one of them is present.
    '''

    dir_path, filename = None, None

    if json_parsed['type'] == 'youtube':
        dir_path, filename = __filepath_tuple(
            f"{recognition_id}-{json_parsed['id']}")
        download_youtube_video(json_parsed['id'], dir_path, filename)
    elif json_parsed['type'] == 'tiktok':
        dir_path, filename = __filepath_tuple(
            f"{recognition_id}-{json_parsed['id']}")
        download_tiktok_video(json_parsed['id'], dir_path, filename)
    else:
        dir_path, filename = __filepath_tuple(
            f"{recognition_id}-{json_parsed['filename']}",
            extension=json_parsed['extension'])
        __dowload_hosted_multimedia(
            json_parsed['url'], f"{dir_path}/{filename}")

    return f"{dir_path}/{filename}"


def __dowload_hosted_multimedia(url, filepath):
    response = requests.get(url, allow_redirects=True)
    open(filepath, 'wb').write(response.content)


def __filepath_tuple(file_name, extension='mp4'):
    project_root_path = Path(__file__).resolve().parent.parent.parent
    dir_path = f"{project_root_path}/resources/multimedia/{os.environ['SPEECH_ENV']}"
    filename = f"{file_name}.{extension}"
    return (dir_path, filename)
