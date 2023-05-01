import json
import logging
import os
from app.muted_stdout_stderr import muted_stdout_stderr
import pycountry
import requests


class GladiaSpeechRecognizer:
    @staticmethod
    def call(filepath, language):
        api_key = os.environ["GLADIA_API_KEY"]

        url = 'https://api.gladia.io/audio/text/audio-transcription/'
        headers = {
            'accept': 'application/json',
            'x-gladia-key': api_key
        }

        files = {
            'audio': (filepath, open(filepath, 'rb'), 'audio/wav'),
            'language': (None, GladiaSpeechRecognizer.get_language_name(language) or 'english'),
            'language_behaviour': (None, 'automatic multiple languages'),
        }

        with muted_stdout_stderr():
            response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            json_body = json.loads(response.text)
            transcription = json_body['prediction'][0]['transcription']
            return transcription if transcription != '' else None
        else:
            logging.getLogger(__name__).error(
                'GladiaSpeechRecognizer error: ' + response.text)
            return

    @staticmethod
    def get_language_name(iso_code):
        try:
            # Extract the first two characters for the ISO 639-1 code
            language = pycountry.languages.get(alpha_2=iso_code[:2])
        except KeyError:
            return None

        if language:
            return language.name.lower()
        else:
            return None
