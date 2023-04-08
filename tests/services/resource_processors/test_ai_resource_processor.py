import logging
from app.services.resource_processors.ai_resource_processor import AiResourceProcessor
import pytest
from unittest.mock import MagicMock, patch


class TestAiResourceProcessor:

    @pytest.fixture
    def input_item_mock(self):
        mock = MagicMock()
        mock.recognition_id = "test_recognition_id"
        mock.resource_id = "test_resource_id"
        mock.save.return_value = "test_filepath"
        mock.recognizer_data = "test_recognizer_data"
        return mock

    @pytest.fixture
    def resource_audio_mock(self):
        with patch('app.services.resource_processors.ai_resource_processor.ResourceAudio') as mock:
            yield mock

    @pytest.fixture
    def temporary_files_cleaner_mock(self):
        with patch('app.services.resource_processors.ai_resource_processor.TemporaryFilesCleaner') as mock:
            yield mock

    def test_call(self, input_item_mock, resource_audio_mock, temporary_files_cleaner_mock):
        # Arrange
        resource_audio_mock.save_as_wav.return_value.split_into_chunks.return_value = None
        resource_audio_mock.save_as_wav.return_value.recognize_all_chunks.return_value.save_subs.return_value = {
            "test_key": "test_value"}
        processor = AiResourceProcessor(input_item_mock)

        # Act
        result = processor.call()

        # Assert
        input_item_mock.save.assert_called_once()
        resource_audio_mock.save_as_wav.assert_called_once_with(
            input_item_mock.recognition_id, "test_filepath")
        resource_audio_mock.save_as_wav.return_value.split_into_chunks.assert_called_once()
        resource_audio_mock.save_as_wav.return_value.recognize_all_chunks.assert_called_once_with(
            input_item_mock.recognizer_data)
        resource_audio_mock.save_as_wav.return_value.recognize_all_chunks.return_value.save_subs.assert_called_once_with(
            input_item_mock.resource_id)
        temporary_files_cleaner_mock.call.assert_called_once_with(
            input_item_mock.recognition_id, "test_filepath")
        assert result == {
            'status': 'ok',
            'input_item.recognition_id': input_item_mock.recognition_id,
            **{"test_key": "test_value"},
        }

    def test_log_step(self, input_item_mock, caplog):
        # Arrange
        processor = AiResourceProcessor(input_item_mock)
        total_steps = 6
        expected_messages = [
            f"[1/{total_steps}] Downloading multimedia from URL ... [{input_item_mock.recognition_id}]",
            f"[2/{total_steps}] Saving audio as WAP ... [{input_item_mock.recognition_id}]",
            f"[3/{total_steps}] Spliting into chunks ... [{input_item_mock.recognition_id}]",
            f"[4/{total_steps}] Recognizing chunks ... [{input_item_mock.recognition_id}]",
            f"[5/{total_steps}] Saving subtitles ... [{input_item_mock.recognition_id}]",
            f"[6/{total_steps}] Cleaning up temporary generated files ... [{input_item_mock.recognition_id}]",
        ]

        # Act
        with caplog.at_level(logging.INFO):
            for i in range(total_steps):
                processor.log_step(i)

        # Assert
        for msg in expected_messages:
            assert msg in caplog.text
