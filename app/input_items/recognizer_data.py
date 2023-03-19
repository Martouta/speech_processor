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

    def __init__(self, language_code, recognizer='google'):
        self.language_code = language_code
        self.recognizer_class = RecognizerData.RECOGNIZER_TYPE_TO_CLASS[recognizer]

    def __str__(self):
        attributes_str = ''
        for item in self.__dict__:
            item_str = '{} = {}'.format(item, self.__dict__[item])
            attributes_str += '\n' + item_str
        return str(self.__class__) + '\n' + attributes_str
