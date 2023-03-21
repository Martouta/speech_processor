from app.input_items.input_item import InputItem
from dataclasses import dataclass
from app.input_items.recognizer_data import RecognizerData


class TestInputItem:
    InputItem.__abstractmethods__ = set()

    @dataclass
    class InputItemDummy(InputItem):
        def __init__(self, resource_id, recognizer_data):
            super().__init__(resource_id=resource_id,
                             recognizer_data=recognizer_data)

        def download(self, dir_path, filename):
            pass

    def test_download(self):
        dummy = TestInputItem.InputItemDummy(
            resource_id=1, recognizer_data=RecognizerData(language_code='en-US'))
        assert dummy.download(dir_path='.', filename='example.txt') is None

    def test_str(self):
        dummy = TestInputItem.InputItemDummy(
            resource_id=1, recognizer_data=RecognizerData(language_code='en-US'))
        dummy_string = dummy.__str__()
        expected_output = (
            "<class 'test_input_item.TestInputItem.InputItemDummy'>\n\n"
            "resource_id = 1\n"
            "recognizer_data = <class 'app.input_items.recognizer_data.RecognizerData'>\n\n"
            "language_code = en-US\n"
            "recognizer_class = <class 'app.services.google_speech_recognizer.GoogleSpeechRecognizer'>\n"
            f"recognition_id = {dummy.recognition_id}\n"
            "extension = None"
        )
        assert dummy_string == expected_output
