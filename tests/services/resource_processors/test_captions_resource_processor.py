import logging
from app.services.resource_processors.captions_resource_processor import CaptionsResourceProcessor
import pytest
from unittest.mock import MagicMock, patch


class TestCaptionsResourceProcessor:
    @pytest.fixture
    def input_item_mock(self):
        mock = MagicMock()
        mock.recognition_id = "test_recognition_id"
        mock.id = "test_id"
        mock.language_code.return_value = "en"
        mock.resource_id = "test_resource_id"
        return mock

    @pytest.fixture
    def youtube_captions_fetcher_mock(self):
        with patch('app.services.resource_processors.captions_resource_processor.YoutubeCaptionsFetcher') as mock:
            yield mock

    def test_call(self, input_item_mock, youtube_captions_fetcher_mock):
        # Arrange
        youtube_captions_fetcher_mock.call.return_value.save_subs.return_value = {
            "test_key": "test_value"}
        processor = CaptionsResourceProcessor(input_item_mock)

        # Act
        result = processor.call()

        # Assert
        youtube_captions_fetcher_mock.call.assert_called_once_with(
            input_item_mock.recognition_id, input_item_mock.id, input_item_mock.language_code()
        )
        youtube_captions_fetcher_mock.call.return_value.save_subs.assert_called_once_with(
            input_item_mock.resource_id)
        assert result == {
            'status': 'ok',
            'input_item.recognition_id': input_item_mock.recognition_id,
            **{"test_key": "test_value"},
        }

    def test_log_step(self, input_item_mock, caplog):
        # Arrange
        processor = CaptionsResourceProcessor(input_item_mock)
        total_steps = 2
        expected_messages = [
            f"[1/{total_steps}] Fetching captions from YouTube ... [{input_item_mock.recognition_id}]",
            f"[2/{total_steps}] Saving subtitles ... [{input_item_mock.recognition_id}]",
        ]

        # Act
        with caplog.at_level(logging.INFO):
            for i in range(total_steps):
                processor.log_step(i)

        # Assert
        for msg in expected_messages:
            assert msg in caplog.text
