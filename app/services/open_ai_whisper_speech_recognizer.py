import openai
import os
import logging


class OpenAIWhisperSpeechRecognizer:
    @staticmethod
    def call(filepath, language):
        try:
            openai.organization_key = os.environ["OPENAI_ORGANIZATION_KEY"]
            openai.api_key = os.environ["OPENAI_API_KEY"]
            audio_file = open(filepath, "rb")
            response_body = openai.Audio.transcribe(
                "whisper-1", audio_file, language=language[0:2])
            return response_body["text"]
        except openai.error.APIError as e:
            logging.error(f"APIError: {str(e)}")
            return None
        except openai.error.AuthenticationError as e:
            logging.error(f"AuthenticationError: {str(e)}")
            return None
