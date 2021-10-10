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
        sp_path = Path(__file__).resolve().parent.parent
        new_path = f"{sp_path}/audios/{os.environ['SPEECH_ENV']}/{name}.wav"
        sound.export(new_path, format='wav')
        return ResourceAudio(recognition_id, AudioSegment.from_wav(new_path))

    def split_into_chunks(self):
        sp_path = Path(__file__).resolve().parent.parent
        path_chunks = f"{sp_path}/audio_chunks/{os.environ['SPEECH_ENV']}/{self.recognition_id}"

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
        sp_path = Path(__file__).resolve().parent.parent
        path_chunks = f"{sp_path}/audio_chunks/{os.environ['SPEECH_ENV']}/{self.recognition_id}"

        google_local = os.getenv('GOOGLE_LOCAL', '1') == '1'

        all_recognitions = []

        for filename in sorted(os.listdir(path_chunks)):
            filepath = f"{path_chunks}/{filename}"
            if google_local:
                response = ResourceAudio.__recognize_local(filepath, language)
                all_recognitions.append(response)
            else:
                response = ResourceAudio.__recognize_cloud(filepath, language)
                for result in response.results:
                    transcript = result.alternatives[0].transcript
                    all_recognitions.append(transcript)

        return Subtitle(self.recognition_id, all_recognitions, language)

    @staticmethod
    def __recognize_local(filepath, language):
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

    @staticmethod
    def __recognize_cloud(filepath, language):
        with io.open(filepath, 'rb') as audiofile:
            info = mediainfo(filepath)
            content = audiofile.read()
            client = speech.SpeechClient()
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code=language,
                sample_rate_hertz=int(info['sample_rate']),
                audio_channel_count=int(info['channels'])
            )
            return client.recognize(config=config, audio=audio)
