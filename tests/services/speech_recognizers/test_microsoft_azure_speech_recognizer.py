import glob
import os
import shutil
from app.services.speech_recognizers.microsoft_azure_speech_recognizer import MicrosoftAzureSpeechRecognizer
import pytest
import httpretty
from unittest.mock import ANY, patch
import speech_recognition as sr


class TestMicrosoftAzureSpeechRecognizer:
    def teardown_method(self):
        for filename in glob.glob(f"{os.getcwd()}/multimedia/test/*.wav"):
            os.remove(filename)

        file_path = f"{os.getcwd()}/resources/audio_chunks/test/recognition_id"
        if os.path.exists(file_path):
            shutil.rmtree(file_path)

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.api_key = "fake-api-key"
        with patch.dict(os.environ, {"MS_AZURE_SPEECH_API_KEY": self.api_key}):
            yield

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_call_success(self):
        filepath = f"{os.getcwd()}/tests/fixtures/example.wav"
        httpretty.register_uri(
            httpretty.POST,
            "https://api.cognitive.microsoft.com/sts/v1.0/issueToken",
            body="{'access_token':'fake_token'}",
            status=200,
        )

        with patch.object(sr.Recognizer, "recognize_azure") as mock_recognize_azure:
            mock_recognize_azure.return_value = "This is a test.", 0

            result = MicrosoftAzureSpeechRecognizer.call(filepath, "en-US")

            mock_recognize_azure.assert_called_once_with(
                ANY, key=self.api_key, language="en-US"
            )
            assert result == "This is a test."

    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_call_exception(self):
        filepath = f"{os.getcwd()}/tests/fixtures/example.wav"
        httpretty.register_uri(
            httpretty.POST,
            "https://api.cognitive.microsoft.com/sts/v1.0/issueToken",
            body="{'access_token':'fake_token'}",
            status=200,
        )

        with patch.object(sr.Recognizer, "recognize_azure") as mock_recognize_azure:
            mock_recognize_azure.side_effect = Exception("API error")

            result = MicrosoftAzureSpeechRecognizer.call(filepath, "en-US")
            assert result is None
