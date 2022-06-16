from app import ResourceAudio
import glob
import httpretty
import os
from pydub import AudioSegment
import re
import shutil


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

    def test_split_into_chunks(self):
        sound = AudioSegment.from_file(
            f"{os.getcwd()}/tests/fixtures/example.wav")
        resource_audio = ResourceAudio('recognition_id', sound)
        chunks_info = resource_audio.split_into_chunks()
        assert f"{os.getcwd()}/resources/audio_chunks/test/recognition_id" == chunks_info['path']
        assert len(glob.glob(
            './resources/audio_chunks/test/recognition_id/chunk*wav')) == chunks_info['number']

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_recognize_all_chunks_google(self):
        filepath = f"{os.getcwd()}/tests/fixtures/example.mp3"
        resource_audio = ResourceAudio.save_as_wav('recognition_id', filepath)
        resource_audio.split_into_chunks()

        expected_recognition = [
            'بخير وانت',
            'شكرا'
        ]
        actual_recognition = []

        httpretty.register_uri(
            httpretty.POST,
            TestResourceAudio.GOOGLE_API_URL,
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

        subtitle = resource_audio.recognize_all_chunks('ar')
        actual_recognition = subtitle.lines

        assert actual_recognition == expected_recognition

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_recognize_chunk_error_unknown_value(self, caplog):
        filepath = f"{os.getcwd()}/tests/fixtures/example.wav"

        httpretty.register_uri(
            httpretty.POST,
            TestResourceAudio.GOOGLE_API_URL,
            adding_headers={
                'content-type': 'audio/x-flac; rate=44100'
            },
            responses=[
                httpretty.Response(
                    '{"result":[{"alternative":[{"confidence":0.00001}],"final":true}],"result_index":0}')
            ]
        )

        recognition = ResourceAudio.recognize_chunk(filepath, 'ar')
        assert '' == recognition

        expected_error = re.escape('speech_recognition.UnknownValueError')
        assert re.search(expected_error, caplog.text, re.MULTILINE)

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_recognize_chunk_error_network_request(self, caplog):
        filepath = f"{os.getcwd()}/tests/fixtures/example.wav"

        httpretty.register_uri(
            httpretty.POST,
            uri=TestResourceAudio.GOOGLE_API_URL,
            status=500
        )

        assert '' == ResourceAudio.recognize_chunk(filepath, 'ar')
        assert re.search('Internal Server Error', caplog.text, re.MULTILINE)
        expected_error = re.escape('speech_recognition.RequestError')
        assert re.search(expected_error, caplog.text, re.MULTILINE)

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
