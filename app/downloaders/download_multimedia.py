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
        fp_tuple = filepath_tuple(
            f"{recognition_id}-{json_parsed['id']}", 'audio')
        dir_path, filename = fp_tuple
        download_youtube_video(json_parsed['id'], fp_tuple)
    elif json_parsed['type'] == 'tiktok':
        fp_tuple = filepath_tuple(
            f"{recognition_id}-{json_parsed['id']}", 'video')
        dir_path, filename = fp_tuple
        download_tiktok_video(json_parsed['id'], fp_tuple)
    else:
        dir_path, filename = filepath_tuple(
            f"{recognition_id}-{json_parsed['filename']}",
            resource_type= 'audio' if (json_parsed['type'] == 'hosted_audio') else 'video',
            extension=json_parsed['extension'])
        __dowload_hosted_multimedia(
            json_parsed['url'], f"{dir_path}/{filename}")

    return f"{dir_path}/{filename}"

def __dowload_hosted_multimedia(url, filepath):
    response = requests.get(url, allow_redirects=True)
    open(filepath, 'wb').write(response.content)


def filepath_tuple(file_name, resource_type='video', extension='mp4'):
    project_root_path = Path(__file__).resolve().parent.parent.parent
    dir_path = f"{project_root_path}/resources/{resource_type}s/{os.environ['SPEECH_ENV']}"
    filename = f"{file_name}.{extension}"
    return (dir_path, filename)
