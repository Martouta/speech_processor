import io
import logging
import os
import re
from pathlib import Path
import requests
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from .subtitle import Subtitle


class ResourceAudio:
    def __init__(self, recognition_id, audio_wav):
        self.recognition_id = recognition_id
        self.audio_wav = audio_wav
        self.path_chunks = f"{Path(__file__).resolve().parent.parent.parent}/" \
            + "resources/audio_chunks/" \
            + f"{os.environ['SPEECH_ENV']}/" \
            + self.recognition_id

    def __str__(self):
        attributes_str = ''
        for item in self.__dict__:
            item_str = '{} = {}'.format(item, self.__dict__[item])
            attributes_str += '\n' + item_str
        return str(self.__class__) + '\n' + attributes_str

    @staticmethod
    def save_as_wav(recognition_id, original_file_path):
        sound = AudioSegment.from_file(original_file_path)
        name = re.match("^.*\\/([^/]*)\\.(mp\\d+|wav)$",
                        original_file_path).group(1)
        sp_path = Path(__file__).resolve().parent.parent.parent
        new_path = f"{sp_path}/resources/multimedia/{os.environ['SPEECH_ENV']}/{name}.wav"
        sound.export(new_path, format='wav')
        return ResourceAudio(recognition_id, AudioSegment.from_wav(new_path))

    def split_into_chunks(self):
        os.mkdir(self.path_chunks)

        chunks = split_on_silence(
            self.audio_wav, min_silence_len=500, silence_thresh=-40)

        for index, chunk in enumerate(chunks, start=0):
            chunk_silent = AudioSegment.silent(duration=10)
            audio_chunk = chunk_silent + chunk + chunk_silent
            filename = f"{self.path_chunks}/chunk{index}.wav"
            audio_chunk.export(filename, bitrate='192k', format='wav')

        return {'number': len(chunks), 'path': self.path_chunks}

    def recognize_all_chunks(self, language):
        all_recognitions = []

        for filename in sorted(os.listdir(self.path_chunks)):
            filepath = f"{self.path_chunks}/{filename}"
            line = ResourceAudio.recognize_chunk(filepath, language)
            all_recognitions.append(line)

        return Subtitle(self.recognition_id, all_recognitions, language)

    @staticmethod
    def recognize_chunk(filepath, language):
        try:
            with sr.AudioFile(filepath) as audiofile:
                recognizer = sr.Recognizer()
                audio = recognizer.record(audiofile)
                return recognizer.recognize_google(audio, language=language)
        except (sr.RequestError, sr.UnknownValueError) as error:
            logging.getLogger(__name__).error(f"{type(error)} - {error}")
            return ''
