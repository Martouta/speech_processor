from app.input_items.input_item_youtube import InputItemYoutube
from app.input_items.recognizer_data import RecognizerData
from app.services.resource_processors.hybrid_resource_processor import HybridResourceProcessor
import pytest
from unittest.mock import patch


class TestHybridResourceProcessor:
    @pytest.fixture
    def input_item(self):
        recognizer_data = RecognizerData(language_code='en-US', captions='try')
        input_item_mock = InputItemYoutube(
            id=id, recognizer_data=recognizer_data, resource_id=55)
        input_item_mock.recognition_id = 'example-recognition-id'
        return input_item_mock

    @pytest.fixture
    def hybrid_resource_processor(self, input_item):
        return HybridResourceProcessor(input_item)

    def test_call_captions_resource_processor_success(self, hybrid_resource_processor, input_item):
        with patch('app.services.resource_processors.captions_resource_processor.CaptionsResourceProcessor.call') as mock_call:
            mock_call.return_value = 'Captions processed'
            assert hybrid_resource_processor.call() == 'Captions processed'
            mock_call.assert_called_once_with()

    def test_call_captions_resource_processor_failure(self, hybrid_resource_processor, input_item):
        with patch('app.services.resource_processors.captions_resource_processor.CaptionsResourceProcessor.call') as captions_mock_call, \
                patch('app.services.resource_processors.ai_resource_processor.AiResourceProcessor.call') as ai_mock_call, \
                patch('logging.info') as log_mock:
            captions_mock_call.side_effect = Exception('Captions Error')
            ai_mock_call.return_value = "AI processed"
            assert hybrid_resource_processor.call() == "AI processed"
            captions_mock_call.assert_called_once_with()
            ai_mock_call.assert_called_once_with()
            log_mock.assert_called_once_with(
                f"[Hybrid] CaptionsResourceProcessor failed for 'example-recognition-id' ...")
