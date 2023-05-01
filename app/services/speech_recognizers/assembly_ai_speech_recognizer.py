import logging
import time
import requests
import os
from app.muted_stdout_stderr import muted_stdout_stderr


class AssemblyAiSpeechRecognizer:
    UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
    TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
    POLLING_ENDPOINT_BASE = "https://api.assemblyai.com/v2/transcript"

    @staticmethod
    def call(filepath, language):
        try:
            with muted_stdout_stderr():
                headers = AssemblyAiSpeechRecognizer._get_headers()
                upload_response = AssemblyAiSpeechRecognizer._upload_file(
                    filepath, headers)
                transcript_response = AssemblyAiSpeechRecognizer._request_transcript(
                    upload_response, headers, language)
                polling_endpoint = AssemblyAiSpeechRecognizer._create_polling_endpoint(
                    transcript_response)
                AssemblyAiSpeechRecognizer._wait_for_completion(
                    polling_endpoint, headers)
                transcribed_text = AssemblyAiSpeechRecognizer._get_transcribed_text(
                    polling_endpoint, headers)

        except Exception as e:
            logging.getLogger(__name__).error(f"Error occurred: {e}")
            transcribed_text = None

        return transcribed_text

    @staticmethod
    def _get_headers():
        api_key = os.environ.get('ASSEMBLYAI_API_KEY')
        headers = {
            'authorization': api_key,
            "content-type": "application/json"
        }
        return headers

    @staticmethod
    def _upload_file(filepath, headers):
        with open(filepath, "rb") as f:
            # Upload the audio file to AssemblyAI
            upload_response = requests.post(
                AssemblyAiSpeechRecognizer.UPLOAD_ENDPOINT,
                headers=headers, data=f.read()
            ).json()
        return upload_response

    @staticmethod
    def _request_transcript(upload_response, headers, language):
        transcript_request = {
            'audio_url': upload_response['upload_url'],
            'language_code': language[:2]
        }
        transcript_response = requests.post(
            AssemblyAiSpeechRecognizer.TRANSCRIPT_ENDPOINT,
            json=transcript_request,
            headers=headers
        ).json()
        return transcript_response

    @staticmethod
    def _create_polling_endpoint(transcript_response):
        polling_endpoint = f"{AssemblyAiSpeechRecognizer.POLLING_ENDPOINT_BASE}/{transcript_response['id']}"
        return polling_endpoint

    @staticmethod
    def _wait_for_completion(polling_endpoint, headers):
        while True:
            polling_response = requests.get(
                polling_endpoint, headers=headers).json()

            if polling_response['status'] == 'completed':
                break

            time.sleep(1)

    @staticmethod
    def _get_transcribed_text(polling_endpoint, headers):
        paragraphs_response = requests.get(
            polling_endpoint + "/paragraphs", headers=headers).json()

        transcribed_text = ''
        for para in paragraphs_response['paragraphs']:
            transcribed_text += para['text'] + '\n'

        return transcribed_text
