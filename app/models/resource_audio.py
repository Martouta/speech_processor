import io
import logging
import os
import re
from pathlib import Path
import speech_recognition as sr
from google.cloud import speech
from pydub import AudioSegment
from pydub.utils import mediainfo
from pydub.silence import split_on_silence
from .subtitle import Subtitle


class ResourceAudio:
    def __init__(self, recognition_id, audio_wav):
        self.recognition_id = recognition_id
        self.audio_wav = audio_wav

    @staticmethod
    def save_as_wav(recognition_id, original_file_path):
        sound = AudioSegment.from_file(original_file_path)
        name = re.match("^.*\\/([^/]*)\\.(mp\\d+|wav)$",
                        original_file_path).group(1)
        sp_path = Path(__file__).resolve().parent.parent.parent
        new_path = f"{sp_path}/resources/audios/{os.environ['SPEECH_ENV']}/{name}.wav"
        sound.export(new_path, format='wav')
        return ResourceAudio(recognition_id, AudioSegment.from_wav(new_path))

    def split_into_chunks(self):
        path_chunks = self.__path_chunks()

        try:
            os.mkdir(path_chunks)
        except FileExistsError:
            pass

        chunks = split_on_silence(
            self.audio_wav, min_silence_len=500, silence_thresh=-40)

        for index, chunk in enumerate(chunks, start=0):
            chunk_silent = AudioSegment.silent(duration=10)
            audio_chunk = chunk_silent + chunk + chunk_silent
            filename = f"{path_chunks}/chunk{index}.wav"
            audio_chunk.export(filename, bitrate='192k', format='wav')

        return {'number': len(chunks), 'path': path_chunks}

    def recognize_chunks(self, language):
        path_chunks = self.__path_chunks()
        all_recognitions = []

        for filename in sorted(os.listdir(path_chunks)):
            filepath = f"{path_chunks}/{filename}"
            line = self.__recognize_chunk(filepath, language)
            all_recognitions.append(line)

        return Subtitle(self.recognition_id, all_recognitions, language)

    def __recognize_chunk(self, filepath, language):
        try:
            with sr.AudioFile(filepath) as audiofile:
                recognizer = sr.Recognizer()
                audio = recognizer.record(audiofile)
                return recognizer.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            return ''
        except sr.RequestError:
            logging.error(
                'Could not request results. check your internet connection')
            return ''

    def __path_chunks(self):
        sp_path = Path(__file__).resolve().parent.parent.parent
        return f"{sp_path}/resources/audio_chunks/{os.environ['SPEECH_ENV']}/{self.recognition_id}"
