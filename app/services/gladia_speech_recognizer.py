import json
import requests
import os
import logging


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
            'language': (None, 'english'), # TODO: change to language
            'language_behaviour': (None, 'automatic multiple languages'),
        }

        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            json_body = json.loads(response.text)
            transcription = json_body['prediction'][0]['transcription']
            return transcription if transcription != '' else None
        else:
            logging.getLogger(__name__).error(
                'GladiaSpeechRecognizer error: ' + response.text)
            return
