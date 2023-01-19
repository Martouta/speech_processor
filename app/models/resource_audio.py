import logging
import os
import re
from pathlib import Path
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from .duration import Duration
from .recognition_line import RecognitionLine
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
        path_regexp = "^.*\\/([^/]*)\\.[^.]*$"
        name = re.match(path_regexp, original_file_path).group(1)
        sound = AudioSegment.from_file(original_file_path)
        sp_path = Path(__file__).resolve().parent.parent.parent
        new_path = f"{sp_path}/resources/multimedia/{os.environ['SPEECH_ENV']}/{name}.wav"
        sound.export(new_path, format='wav')
        return ResourceAudio(recognition_id, AudioSegment.from_wav(new_path))

    def split_into_chunks(self):
        os.mkdir(self.path_chunks)

        chunks = split_on_silence(
            self.audio_wav, min_silence_len=400, silence_thresh=-40)

        start_time = 0
        for index, chunk in enumerate(chunks, start=0):
            self._export_audio_chunk(chunk, index)
            start_time = self._export_ts_chunk(chunk, start_time, index)

        return {'number': len(chunks), 'path': self.path_chunks}

    def _export_audio_chunk(self, chunk, index):
        chunk_silent = AudioSegment.silent(duration=10)
        audio_chunk = chunk_silent + chunk + chunk_silent
        filename = f"{self.path_chunks}/chunk{index}.wav"
        audio_chunk.export(filename, bitrate='192k', format='wav')

    def _export_ts_chunk(self, chunk, start_time, index):
        end_time = start_time + (chunk.duration_seconds * 1000)
        filename = f"{self.path_chunks}/chunk{index}.txt"
        Duration(start_time, end_time).export(filename, index)
        return end_time

    def recognize_all_chunks(self, language):
        all_recognitions = []

        for filename in sorted(os.listdir(self.path_chunks)):
            recognition_line = self._recognize_chunk(language, filename)
            if recognition_line:
                all_recognitions.append(recognition_line)

        return Subtitle(self.recognition_id, all_recognitions, language)

    def _recognize_chunk(self, language, filename):
        root, extension = os.path.splitext(filename)

        if extension != ".wav":
            return

        filepath_wav = f"{self.path_chunks}/{filename}"
        line_text = ResourceAudio.recognize_chunk(filepath_wav, language)
        filepath_ts = f"{self.path_chunks}/{root}.txt"

        with open(filepath_ts, 'r') as ts_file:
            _, ts_start, ts_end = ts_file.read().split(";")
            duration = Duration.from_srt(ts_start, ts_end)
            recognition_line = RecognitionLine(line_text, duration)
            return recognition_line

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
