from app.services.assembly_ai_speech_recognizer import AssemblyAiSpeechRecognizer
from app.services.gladia_speech_recognizer import GladiaSpeechRecognizer
from app.services.google_speech_recognizer import GoogleSpeechRecognizer
from app.services.microsoft_azure_speech_recognizer import MicrosoftAzureSpeechRecognizer
from app.services.open_ai_whisper_speech_recognizer import OpenAIWhisperSpeechRecognizer


class RecognizerData:
    RECOGNIZER_TYPE_TO_CLASS = {
        'assemblyai':  AssemblyAiSpeechRecognizer,
        'gladia': GladiaSpeechRecognizer,
        'google':  GoogleSpeechRecognizer,
        'microsoft':  MicrosoftAzureSpeechRecognizer,
        'openai':  OpenAIWhisperSpeechRecognizer
    }

    def __init__(self, language_code, recognizer='google', captions=False):
        self.language_code = language_code
        self.recognizer_class = RecognizerData.RECOGNIZER_TYPE_TO_CLASS[recognizer or 'google']
        self._captions = captions or False

    def are_captions_requested(self):
        return self._captions

    def __str__(self):
        attributes_str = ''
        for item in self.__dict__:
            item_str = '{} = {}'.format(item, self.__dict__[item])
            attributes_str += '\n' + item_str
        return str(self.__class__) + '\n' + attributes_str

    def __eq__(self, other):
        if isinstance(other, RecognizerData):
            return self.recognizer_class == other.recognizer_class and self.language_code == other.language_code
        return False
