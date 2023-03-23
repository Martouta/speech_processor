import pytest
from app import RecognizerData
from app.services.assembly_ai_speech_recognizer import AssemblyAiSpeechRecognizer
from app.services.gladia_speech_recognizer import GladiaSpeechRecognizer
from app.services.google_speech_recognizer import GoogleSpeechRecognizer
from app.services.microsoft_azure_speech_recognizer import MicrosoftAzureSpeechRecognizer
from app.services.open_ai_whisper_speech_recognizer import OpenAIWhisperSpeechRecognizer


class TestRecognizerData:
    @pytest.mark.parametrize("recognizer, expected_class", [
        ('assemblyai', AssemblyAiSpeechRecognizer),
        ('gladia', GladiaSpeechRecognizer),
        ('google', GoogleSpeechRecognizer),
        ('microsoft', MicrosoftAzureSpeechRecognizer),
        ('openai', OpenAIWhisperSpeechRecognizer),
    ])
    def test_recognizer_class(self, recognizer, expected_class):
        recognizer_data = RecognizerData('en-US', recognizer)
        assert recognizer_data.recognizer_class == expected_class

    def test_default_recognizer_class(self):
        recognizer_data = RecognizerData('en-US')
        assert recognizer_data.recognizer_class == GoogleSpeechRecognizer

    def test_init_language_code(self):
        recognizer_data = RecognizerData('en-US')
        assert recognizer_data.language_code == 'en-US'

    def test_str_representation(self):
        recognizer_data = RecognizerData('en-US', 'google')
        expected_str = (
            f"<class '{RecognizerData.__module__}.{RecognizerData.__name__}'>\n\n"
            'language_code = en-US\n'
            "recognizer_class = <class 'app.services.google_speech_recognizer.GoogleSpeechRecognizer'>\n"
            '_captions = False'
        )
        assert str(recognizer_data) == expected_str

    @pytest.mark.parametrize("captions, expected", [
        (True, True),
        (False, False),
        (None, False),
    ])
    def test_are_captions_requested(self, captions, expected):
        recognizer_data = RecognizerData('en-US', captions=captions)
        assert recognizer_data.are_captions_requested() == expected

    def test_invalid_recognizer_type(self):
        with pytest.raises(KeyError):
            RecognizerData('en-US', 'invalid_recognizer')

    def test_eq_same_instance(self):
        recognizer_data1 = RecognizerData('en-US', 'google')
        assert recognizer_data1 == recognizer_data1

    def test_eq_different_instances_same_values(self):
        recognizer_data1 = RecognizerData('en-US', 'google')
        recognizer_data2 = RecognizerData('en-US', 'google')
        assert recognizer_data1 == recognizer_data2

    def test_eq_different_language_code(self):
        recognizer_data1 = RecognizerData('en-US', 'google')
        recognizer_data2 = RecognizerData('es-ES', 'google')
        assert recognizer_data1 != recognizer_data2

    def test_eq_different_recognizer_class(self):
        recognizer_data1 = RecognizerData('en-US', 'google')
        recognizer_data2 = RecognizerData('en-US', 'openai')
        assert recognizer_data1 != recognizer_data2

    def test_eq_different_class(self):
        recognizer_data = RecognizerData('en-US', 'google')
        assert recognizer_data != 'some_string'
