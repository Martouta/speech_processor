import json
import os
from unittest import mock
from app.services.speech_recognizers.open_ai_whisper_speech_recognizer import OpenAIWhisperSpeechRecognizer
import openai
import httpretty


class TestOpenAIWhisperSpeechRecognizer:
    WHISPER_API_URL = "https://api.openai.com/v1/audio/transcriptions"

    @httpretty.activate(verbose=True, allow_net_connect=False)
    @mock.patch.dict(os.environ, {'OPENAI_ORGANIZATION_KEY': 'EXAMPLE_ORGANIZATION_KEY'})
    @mock.patch.dict(os.environ, {'OPENAI_API_KEY': 'EXAMPLE_API_KEY'})
    def test_successful_transcription(self):
        httpretty.register_uri(
            httpretty.POST,
            TestOpenAIWhisperSpeechRecognizer.WHISPER_API_URL,
            status=200,
            body=json.dumps({"text": "test transcription", "status": "ok"}),
        )
        result = OpenAIWhisperSpeechRecognizer.call(
            f"{os.getcwd()}/tests/fixtures/example.wav", "en-US"
        )
        assert result == "test transcription"

    @httpretty.activate(verbose=True, allow_net_connect=False)
    @mock.patch.dict(os.environ, {'OPENAI_ORGANIZATION_KEY': 'EXAMPLE_ORGANIZATION_KEY'})
    @mock.patch.dict(os.environ, {'OPENAI_API_KEY': 'EXAMPLE_API_KEY'})
    def test_api_error_logging(self, caplog):
        with mock.patch.object(openai.Audio, "transcribe") as mock_transcribe:
            mock_transcribe.side_effect = openai.error.APIError(
                "Bad Request (status 400)",
                headers={"content-type": "application/json"},
            )

            result = OpenAIWhisperSpeechRecognizer.call(
                f"{os.getcwd()}/tests/fixtures/example.wav", "en"
            )
            assert result is None
            assert "APIError" in caplog.text
            assert "400" in caplog.text

    @httpretty.activate(verbose=True, allow_net_connect=False)
    @mock.patch.dict(os.environ, {'OPENAI_ORGANIZATION_KEY': 'EXAMPLE_ORGANIZATION_KEY'})
    @mock.patch.dict(os.environ, {'OPENAI_API_KEY': 'INVALID_API_KEY'})
    def test_authentication_error_logging(self, caplog):
        with mock.patch.object(openai.Audio, "transcribe") as mock_transcribe:
            mock_transcribe.side_effect = openai.error.AuthenticationError(
                "Incorrect API key provided (status 401)",
                headers={"content-type": "application/json"},
            )
            result = OpenAIWhisperSpeechRecognizer.call(
                f"{os.getcwd()}/tests/fixtures/example.wav", "en"
            )
            assert result is None
            assert "AuthenticationError" in caplog.text
            assert "status 401" in caplog.text
