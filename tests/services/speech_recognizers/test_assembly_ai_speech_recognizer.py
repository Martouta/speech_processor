import os
import shutil
import glob
import httpretty
from unittest.mock import patch
from app import AssemblyAiSpeechRecognizer


class TestAssemblyAiSpeechRecognizer:
    def teardown_method(self):
        for filename in glob.glob(f"{os.getcwd()}/multimedia/test/*.wav"):
            os.remove(filename)

        file_path = f"{os.getcwd()}/resources/audio_chunks/test/recognition_id"
        if os.path.exists(file_path):
            shutil.rmtree(file_path)

    @httpretty.activate(verbose=True, allow_net_connect=False)
    @patch.dict(os.environ, {'ASSEMBLYAI_API_KEY': 'test_key'})
    def test_transcribe_success(self):
        audio_file_path = f"{os.getcwd()}/tests/fixtures/example.wav"
        upload_url = "https://api.assemblyai.com/v2/upload"
        transcript_url = "https://api.assemblyai.com/v2/transcript"
        polling_url = "https://api.assemblyai.com/v2/transcript/test_id"
        paragraphs_url = "https://api.assemblyai.com/v2/transcript/test_id/paragraphs"

        httpretty.register_uri(
            httpretty.POST,
            upload_url,
            body='{"upload_url": "https://aws.com/test_audio"}',
            content_type="application/json"
        )

        httpretty.register_uri(
            httpretty.POST,
            transcript_url,
            body='{"id": "test_id"}',
            content_type="application/json"
        )

        httpretty.register_uri(
            httpretty.GET,
            polling_url,
            responses=[
                httpretty.Response(
                    body='{"status": "queued"}', content_type="application/json"),
                httpretty.Response(
                    body='{"status": "processing"}', content_type="application/json"),
                httpretty.Response(
                    body='{"status": "completed"}', content_type="application/json"),
            ]
        )

        httpretty.register_uri(
            httpretty.GET,
            paragraphs_url,
            body='{"paragraphs": [{"text": "This is a test transcription."}]}',
            content_type="application/json"
        )

        transcribed_text = AssemblyAiSpeechRecognizer.call(
            audio_file_path, 'en-US')
        assert transcribed_text == "This is a test transcription.\n"

    @httpretty.activate(verbose=True, allow_net_connect=False)
    @patch.dict(os.environ, {'ASSEMBLYAI_API_KEY': 'test_key'})
    def test_transcribe_failure(self):
        audio_file_path = f"{os.getcwd()}/tests/fixtures/example.wav"
        upload_url = "https://api.assemblyai.com/v2/upload"
        transcript_url = "https://api.assemblyai.com/v2/transcript"

        httpretty.register_uri(
            httpretty.POST,
            upload_url,
            body='{"upload_url": "https://aws.com/test_audio"}',
            content_type="application/json"
        )

        httpretty.register_uri(
            httpretty.POST,
            transcript_url,
            status=500
        )

        transcribed_text = AssemblyAiSpeechRecognizer.call(
            audio_file_path, 'en-US')
        assert transcribed_text is None
