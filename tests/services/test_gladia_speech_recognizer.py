import json
import logging
import os
import glob
import shutil
import httpretty
from unittest import mock
from app import GladiaSpeechRecognizer


class TestGladiaSpeechRecognizer:
    GLADIA_API_URL = "https://api.gladia.io/audio/text/audio-transcription/"

    def teardown_method(self):
        for filename in glob.glob(f"{os.getcwd()}/multimedia/test/*.wav"):
            os.remove(filename)

        file_path = f"{os.getcwd()}/resources/audio_chunks/test/recognition_id"
        if os.path.exists(file_path):
            shutil.rmtree(file_path)

    @mock.patch.dict(os.environ, {'GLADIA_API_KEY': 'EXAMPLE_API_KEY'})
    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_call_success(self):
        # Arrange
        test_filepath = f"{os.getcwd()}/tests/fixtures/example.wav"
        httpretty.register_uri(
            httpretty.POST,
            TestGladiaSpeechRecognizer.GLADIA_API_URL,
            body=json.dumps({
                'prediction': [{'transcription': 'This is a test transcription.'}]
            }),
            content_type='application/json',
            status=200
        )

        # Act
        result = GladiaSpeechRecognizer.call(test_filepath, 'english')

        # Assert
        assert result == 'This is a test transcription.'

    @mock.patch.dict(os.environ, {'GLADIA_API_KEY': 'EXAMPLE_API_KEY'})
    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_call_empty_transcription(self):
        # Arrange
        test_filepath = f"{os.getcwd()}/tests/fixtures/example.wav"
        httpretty.register_uri(
            httpretty.POST,
            TestGladiaSpeechRecognizer.GLADIA_API_URL,
            body=json.dumps({
                'prediction': [{'transcription': ''}]
            }),
            content_type='application/json',
            status=200
        )

        # Act
        result = GladiaSpeechRecognizer.call(test_filepath, 'english')

        # Assert
        assert result is None

    @mock.patch.dict(os.environ, {'GLADIA_API_KEY': 'EXAMPLE_API_KEY'})
    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_call_error(self, caplog):
        # Arrange
        test_filepath = f"{os.getcwd()}/tests/fixtures/example.wav"
        error_message = 'GladiaSpeechRecognizer error: Invalid API key'
        httpretty.register_uri(
            httpretty.POST,
            TestGladiaSpeechRecognizer.GLADIA_API_URL,
            body=error_message,
            content_type='application/json',
            status=400
        )

        # Act
        with caplog.at_level(logging.ERROR):
            result = GladiaSpeechRecognizer.call(test_filepath, 'english')

        # Assert
        assert result is None
        assert error_message in caplog.text
