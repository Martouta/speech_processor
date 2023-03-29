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
        recognizer_data = RecognizerData(language_code='en-US')
        dummy = TestInputItem.InputItemDummy(
            resource_id=1, recognizer_data=recognizer_data)
        dummy_string = dummy.__str__()
        expected_output = (
            "<class 'test_input_item.TestInputItem.InputItemDummy'>\n\n"
            "resource_id = 1\n"
            f"recognizer_data = {str(recognizer_data)}\n"
            f"recognition_id = {dummy.recognition_id}\n"
            "extension = None"
        )
        assert dummy_string == expected_output

    def test_are_captions_requested(self):
        recognizer_data = RecognizerData(language_code='en-US')
        item_without_captions = TestInputItem.InputItemDummy(
            resource_id=1, recognizer_data=recognizer_data)
        assert not item_without_captions.are_captions_requested()

        recognizer_data = RecognizerData(language_code='en-US', captions=True)
        item_without_captions = TestInputItem.InputItemDummy(
            resource_id=1, recognizer_data=recognizer_data)
        assert item_without_captions.are_captions_requested()

    def test_language_code(self):
        recognizer_data = RecognizerData(language_code='en-US')
        dummy = TestInputItem.InputItemDummy(
            resource_id=1, recognizer_data=recognizer_data)
        assert dummy.language_code() == 'en-US'
