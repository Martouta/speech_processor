from dataclasses import dataclass
import os
import re
from unittest.mock import patch
from app.input_items.input_item import InputItem
from app.input_items.recognizer_data import RecognizerData


class TestInputItem:
    InputItem.__abstractmethods__ = set()

    @dataclass
    class InputItemDummy(InputItem):
        def __init__(self, resource_id, recognizer_data):
            super().__init__(resource_id=resource_id,
                             recognizer_data=recognizer_data)

        def download(self, filename):
            pass

    def test_save(self):
        recognizer_data = RecognizerData(language_code='en-US')
        dummy = TestInputItem.InputItemDummy(
            resource_id=1, recognizer_data=recognizer_data)
        expected_filepath_regexp = r'^' + re.escape(f"{os.getcwd()}/") \
            + re.escape('resources/multimedia/') \
            + re.escape(os.environ['SPEECH_ENV']) \
            + '/' \
            + r'\d+-1-' \
            + r'\d{2}-\d{2}\.\d{2}:\d{2}:\d+\.None$'

        with patch.object(dummy, 'download', autospec=True) as mock_download:
            mock_download.return_value = None
            filepath = dummy.save()
            assert re.match(expected_filepath_regexp, filepath)
            mock_download.assert_called_once_with(filepath)

    def test_download(self):
        dummy = TestInputItem.InputItemDummy(
            resource_id=1, recognizer_data=RecognizerData(language_code='en-US'))
        assert dummy.download(filename='./example.txt') is None

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

    def test_language_code(self):
        recognizer_data = RecognizerData(language_code='en-US')
        dummy = TestInputItem.InputItemDummy(
            resource_id=1, recognizer_data=recognizer_data)
        assert dummy.language_code() == 'en-US'

    def test_call_resource_processor(self):
        recognizer_data = RecognizerData(language_code='en-US', captions='try')
        dummy = TestInputItem.InputItemDummy(
            resource_id=1, recognizer_data=recognizer_data)

        with patch('app.services.resource_processors.hybrid_resource_processor.HybridResourceProcessor.call') as mock_call:
            mock_call.return_value = 'Processed resource'
            assert dummy.call_resource_processor() == 'Processed resource'
            mock_call.assert_called_once_with()
