from app import ResourceAudio
import glob
from app.input_items.recognizer_data import RecognizerData
from app.services.google_speech_recognizer import GoogleSpeechRecognizer
import httpretty
import os
from pydub import AudioSegment
import pydub
import re
import shutil
import pytest


class TestResourceAudio:
    GOOGLE_API_URL = 'http://www.google.com/speech-api/v2/recognize?client=chromium&lang=ar&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw'

    def teardown_method(self):
        for filename in glob.glob(f"{os.getcwd()}/multimedia/test/*.wav"):
            os.remove(filename)

        file_path = f"{os.getcwd()}/resources/audio_chunks/test/recognition_id"
        if os.path.exists(file_path):
            shutil.rmtree(file_path)

    def assert_save_wav_for(self, format):
        name = 'example'
        filepath = f"{os.getcwd()}/tests/fixtures/{name}.{format}"
        resource_audio = ResourceAudio.save_as_wav('recognition_id', filepath)
        assert os.path.exists(f"resources/multimedia/test/{name}.wav") == 1
        assert type(resource_audio) == ResourceAudio

    def test_save_as_wav_for_mp3(self):
        self.assert_save_wav_for(format='mp3')

    def test_save_as_wav_for_mp4(self):
        self.assert_save_wav_for(format='mp4')

    def test_save_as_wav_for_wav(self):
        self.assert_save_wav_for(format='wav')

    def test_save_as_wav_non_existent(self):
        filepath = f"{os.getcwd()}/tests/fixtures/fake.fake"
        with pytest.raises(FileNotFoundError):
            ResourceAudio.save_as_wav('recognition_id', filepath)

    def test_save_as_wav_invalid_format(self):
        filepath = f"{os.getcwd()}/tests/fixtures/example.txt"
        with pytest.raises(pydub.exceptions.CouldntDecodeError):
            ResourceAudio.save_as_wav('recognition_id', filepath)

    def test_split_into_chunks(self):
        sound = AudioSegment.from_file(
            f"{os.getcwd()}/tests/fixtures/example.wav")
        resource_audio = ResourceAudio('recognition_id', sound)
        chunks_info = resource_audio.split_into_chunks()
        assert f"{os.getcwd()}/resources/audio_chunks/test/recognition_id" == chunks_info['path']
        assert len(glob.glob(
            './resources/audio_chunks/test/recognition_id/chunk*wav')) == chunks_info['number']
        assert len(glob.glob(
            './resources/audio_chunks/test/recognition_id/chunk*txt')) == chunks_info['number']
        expected_ts = [
            '0;00:00:00,000;00:00:01,328',
            '1;00:00:01,328;00:00:01,928'
        ]
        for i in range(chunks_info['number']):
            ts_chunk_fp = f"./resources/audio_chunks/test/recognition_id/chunk{i}.txt"
            assert os.path.exists(ts_chunk_fp)
            with open(ts_chunk_fp, 'r') as file:
                assert file.read() == expected_ts[i]

    def setup_recognize_all_chunks(self, filepath):
        resource_audio = ResourceAudio.save_as_wav('recognition_id', filepath)
        resource_audio.split_into_chunks()
        return resource_audio

    def register_google_api_responses(self, responses):
        httpretty.register_uri(
            httpretty.POST,
            TestResourceAudio.GOOGLE_API_URL,
            adding_headers={
                'content-type': 'audio/x-flac; rate=44100'
            },
            responses=responses
        )

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_recognize_all_chunks_google_with_correct_transcripts(self):
        filepath = f"{os.getcwd()}/tests/fixtures/example.mp3"
        resource_audio = self.setup_recognize_all_chunks(filepath)

        expected_recognition = [
            '00:00:00,000;00:00:01,328;بخير وانت',
            '00:00:01,328;00:00:01,928;شكرا'
        ]

        responses = [
            httpretty.Response(
                '{"result":[{"alternative":[{"transcript":"بخير وانت","confidence":0.85492837}],"final":true}],"result_index":0}'),
            httpretty.Response(
                '{"result":[{"alternative":[{"transcript":"شكرا","confidence":0.5705713}],"final":true}],"result_index":0}')
        ]

        self.register_google_api_responses(responses)

        recognizer_data = RecognizerData('ar', 'google')
        subtitle = resource_audio.recognize_all_chunks(recognizer_data)

        assert list(map(lambda recognition_line: str(
            recognition_line), subtitle.lines)) == expected_recognition

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_recognize_all_chunks_google_with_mix_correct_incorrect_transcripts(self):
        filepath = f"{os.getcwd()}/tests/fixtures/example.mp3"
        resource_audio = self.setup_recognize_all_chunks(filepath)

        expected_recognition = [
            '00:00:01,328;00:00:01,928;شكرا'
        ]

        responses = [
            httpretty.Response(
                '{"result":[{"alternative":[{"confidence":0.00001}],"final":true}],"result_index":0}'),
            httpretty.Response(
                '{"result":[{"alternative":[{"transcript":"شكرا","confidence":0.5705713}],"final":true}],"result_index":0}')
        ]

        self.register_google_api_responses(responses)

        recognizer_data = RecognizerData('ar', 'google')
        subtitle = resource_audio.recognize_all_chunks(recognizer_data)

        assert list(map(lambda recognition_line: str(
            recognition_line), subtitle.lines)) == expected_recognition

    def test_str(self):
        sound = AudioSegment.from_file(
            f"{os.getcwd()}/tests/fixtures/example.wav")
        resource_audio = ResourceAudio('test_recognition_id', sound)
        expected_output = re.escape("<class 'app.models.resource_audio.ResourceAudio'>\n") \
            + r"\n" \
            + r"recognition_id = test_recognition_id\n" \
            + r"audio_wav = <pydub\.audio_segment\.AudioSegment object at 0[xX][0-9a-fA-F]+>"
        assert re.match(expected_output,
                        resource_audio.__str__(), re.MULTILINE)
