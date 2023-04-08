import glob
from app.models.resource_audio import ResourceAudio
from app.services.speech_recognizers.google_speech_recognizer import GoogleSpeechRecognizer
import httpretty
import os
import re
import shutil


class TestGoogleSpeechRecognizer:
    GOOGLE_API_URL = 'http://www.google.com/speech-api/v2/recognize?client=chromium&lang=ar&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw'

    def teardown_method(self):
        for filename in glob.glob(f"{os.getcwd()}/multimedia/test/*.wav"):
            os.remove(filename)

        file_path = f"{os.getcwd()}/resources/audio_chunks/test/recognition_id"
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
    
    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_recognize_chunk_google_with_correct_transcript(self):
        filepath = f"{os.getcwd()}/tests/fixtures/example.mp3"
        resource_audio = ResourceAudio.save_as_wav('recognition_id', filepath)
        resource_audio.split_into_chunks()

        httpretty.register_uri(
            httpretty.POST,
            TestGoogleSpeechRecognizer.GOOGLE_API_URL,
            adding_headers={
                'content-type': 'audio/x-flac; rate=44100'
            },
            responses=[
                httpretty.Response(
                    '{"result":[{"alternative":[{"transcript":"شكرا","confidence":0.5705713}],"final":true}],"result_index":0}')
            ]
        )

        recognition_text =  GoogleSpeechRecognizer.call(filepath, 'ar')
        assert "شكرا" == recognition_text

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_recognize_chunk_error_unknown_value(self, caplog):
        filepath = f"{os.getcwd()}/tests/fixtures/example.wav"

        httpretty.register_uri(
            httpretty.POST,
            TestGoogleSpeechRecognizer.GOOGLE_API_URL,
            adding_headers={
                'content-type': 'audio/x-flac; rate=44100'
            },
            responses=[
                httpretty.Response(
                    '{"result":[{"alternative":[{"confidence":0.00001}],"final":true}],"result_index":0}')
            ]
        )

        recognition_text =  GoogleSpeechRecognizer.call(filepath, 'ar')
        assert recognition_text is None

        expected_error = re.escape('speech_recognition.UnknownValueError')
        assert re.search(expected_error, caplog.text, re.MULTILINE)

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_recognize_chunk_error_network_request(self, caplog):
        filepath = f"{os.getcwd()}/tests/fixtures/example.wav"

        httpretty.register_uri(
            httpretty.POST,
            uri=TestGoogleSpeechRecognizer.GOOGLE_API_URL,
            status=500
        )

        recognition_text =  GoogleSpeechRecognizer.call(filepath, 'ar')
        assert recognition_text is None
        assert re.search('Internal Server Error', caplog.text, re.MULTILINE)
        expected_error = re.escape('speech_recognition.RequestError')
        assert re.search(expected_error, caplog.text, re.MULTILINE)
