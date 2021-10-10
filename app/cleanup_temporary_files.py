import os
import re
import shutil
from pathlib import Path


def cleanup_temporary_files(recognition_id, downloaded_multimedia_path):
    '''
    Cleanup after usage:
    1. Downloaded video/audio.
    2. WAV equivalent.
    3. audio_chunks folder created for this recognition.
    '''

    speech_env = os.environ['SPEECH_ENV']
    sp_path = Path(__file__).resolve().parent.parent
    name = re.match("^.*\\/([^/]*)\\.(mp\\d+|wav)$",
                    downloaded_multimedia_path).group(1)
    wav_path = f"{sp_path}/audios/{speech_env}/{name}.wav"

    for file_path in [downloaded_multimedia_path, wav_path]:
        if os.path.exists(file_path):
            os.remove(file_path)

    audio_chunks_path = f"{sp_path}/audio_chunks/{speech_env}/{recognition_id}"
    if os.path.exists(audio_chunks_path):
        shutil.rmtree(audio_chunks_path)
