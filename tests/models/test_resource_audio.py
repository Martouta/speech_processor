import httpretty
import pytest
from unittest import mock
import os
import glob
import requests
import requests_mock
import shutil
from pydub import AudioSegment
import app
from app import ResourceAudio


class TestResourceAudio:
    def teardown_method(self):
        for filename in glob.glob('audios/test/*.wav'):
            os.remove(filename)

        file_path = f"{os.getcwd()}/resources/audio_chunks/test/recognition_id"
        if os.path.exists(file_path):
            shutil.rmtree(file_path)

    def assert_save_wav_for(self, format):
        name = 'example'
        filepath = f"{os.getcwd()}/tests/fixtures/{name}.{format}"
        resource_audio = ResourceAudio.save_as_wav('recognition_id', filepath)
        assert os.path.exists(f"resources/audios/test/{name}.wav") == 1
        assert type(resource_audio) == ResourceAudio

    def test_save_as_wav_for_mp3(self):
        self.assert_save_wav_for(format='mp3')

    def test_save_as_wav_for_mp4(self):
        self.assert_save_wav_for(format='mp4')

    def test_save_as_wav_for_wav(self):
        self.assert_save_wav_for(format='wav')

    def test_split_into_chunks(self):
        filepath = f"{os.getcwd()}/tests/fixtures/example.wav"
        sound = AudioSegment.from_file(filepath)
        resource_audio = ResourceAudio('recognition_id', sound)
        chunks_info = resource_audio.split_into_chunks()
        assert f"{os.getcwd()}/resources/audio_chunks/test/recognition_id" == chunks_info['path']
        assert len(glob.glob(
            './resources/audio_chunks/test/recognition_id/chunk*wav')) == chunks_info['number']

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_recognize_chunks_google(self):
        filepath = f"{os.getcwd()}/tests/fixtures/example.mp3"
        resource_audio = ResourceAudio.save_as_wav('recognition_id', filepath)
        resource_audio.split_into_chunks()

        expected_recognition = [
            'بخير وانت',
            'شكرا'
        ]
        actual_recognition = []

        api_url = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang=ar&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
        httpretty.register_uri(
            httpretty.POST,
            api_url,
            adding_headers={
                'content-type': 'audio/x-flac; rate=44100'
            },
            responses=[
                httpretty.Response(
                    '{"result":[{"alternative":[{"transcript":"بخير وانت","confidence":0.85492837}],"final":true}],"result_index":0}'),
                httpretty.Response(
                    '{"result":[{"alternative":[{"transcript":"شكرا","confidence":0.5705713}],"final":true}],"result_index":0}')
            ]
        )

        subtitle = resource_audio.recognize_chunks('ar')
        actual_recognition = subtitle.lines

        assert actual_recognition == expected_recognition
