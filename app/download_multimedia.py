import os
from pathlib import Path
import requests
from pytube import YouTube


def download_multimedia(recognition_id, json_parsed):
    '''
    Download video or audio from URL and returns the path where it has been saved.
    If there is a video, it downloads it, otherwise, it goes for the audio.
    It assumes that at least one of them is present.
    '''

    dir_path, filename = None, None

    if 'youtube_reference_id' in json_parsed and json_parsed['youtube_reference_id']:
        fp_tuple = filepath_tuple(
            f"{recognition_id}-{json_parsed['youtube_reference_id']}", 'audio')
        dir_path, filename = fp_tuple
        __download_youtube_video(json_parsed['youtube_reference_id'], fp_tuple)
    else:
        resource_data, resource_type = __attachment_data(json_parsed)
        dir_path, filename = filepath_tuple(
            f"{recognition_id}-{resource_data['filename']}",
            resource_type=resource_type,
            extension=resource_data['extension'])
        __dowload_hosted_multimedia(
            resource_data['url'], f"{dir_path}/{filename}")

    return f"{dir_path}/{filename}"


def __download_youtube_video(reference_id, fp_tuple):
    YouTube(f"youtube.com/watch?v={reference_id}") \
        .streams \
        .filter(only_audio=True, file_extension='mp4') \
        .order_by('abr') \
        .desc() \
        .first() \
        .download(output_path=fp_tuple[0], filename=fp_tuple[1])


def __dowload_hosted_multimedia(url, filepath):
    response = requests.get(url, allow_redirects=True)
    open(filepath, 'wb').write(response.content)


def filepath_tuple(file_name, resource_type='video', extension='mp4'):
    project_root_path = Path(__file__).resolve().parent.parent
    dir_path = f"{project_root_path}/{resource_type}s/{os.environ['SPEECH_ENV']}"
    filename = f"{file_name}.{extension}"
    return (dir_path, filename)


def __attachment_data(json_parsed):
    if json_parsed.get('video') and json_parsed['video']['url']:
        return (json_parsed['video'], 'video')

    return (json_parsed['audio'], 'audio')
