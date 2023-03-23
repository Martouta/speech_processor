import json
import pytest
from unittest.mock import MagicMock, patch
from app.models.duration import Duration
from app.models.recognition_line import RecognitionLine
from app.models.subtitle import Subtitle
from app.services.youtube_captions_fetcher import YoutubeCaptionsFetcher


class TestYoutubeCaptionsFetcher:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.video_id = "test_video_id"
        self.language = "en-US"

    def test_call_success(self):
        expected_subtitle = Subtitle(
            recognition_id=self.video_id,
            lines=[
                RecognitionLine("Hello, world!", Duration(0, 1.5)),
                RecognitionLine("How are you?", Duration(1.5, 3.0)),
            ],
            language=self.language,
        )

        with patch("app.services.youtube_captions_fetcher.YouTubeTranscriptApi") as mock_youtube_api:
            mock_transcript = MagicMock()
            mock_transcript.language_code = self.language[:2]
            mock_transcript.is_generated = False
            mock_youtube_api.list_transcripts.return_value = [mock_transcript]

            mock_json_formatter = MagicMock()
            mock_json_formatter.format_transcript.return_value = json.dumps([
                {"start": 0, "duration": 1.5, "text": "Hello, world!"},
                {"start": 1.5, "duration": 1.5, "text": "How are you?"},
            ])

            with patch("app.services.youtube_captions_fetcher.JSONFormatter", return_value=mock_json_formatter):
                subtitle = YoutubeCaptionsFetcher.call(
                    self.video_id, self.language)

        assert subtitle == expected_subtitle

    def test_call_no_manual_captions(self):
        with patch("app.services.youtube_captions_fetcher.YouTubeTranscriptApi") as mock_youtube_api:
            mock_transcript = MagicMock()
            mock_transcript.language_code = self.language[:2]
            mock_transcript.is_generated = True
            mock_youtube_api.list_transcripts.return_value = [mock_transcript]

            with pytest.raises(ValueError) as exc_info:
                YoutubeCaptionsFetcher.call(self.video_id, self.language)

        assert str(
            exc_info.value) == f"No manual captions found for video ID {self.video_id} and language {self.language}"

    def test_call_wrong_language(self):
        with patch("app.services.youtube_captions_fetcher.YouTubeTranscriptApi") as mock_youtube_api:
            mock_transcript = MagicMock()
            mock_transcript.language_code = "es"
            mock_transcript.is_generated = False
            mock_youtube_api.list_transcripts.return_value = [mock_transcript]

            with pytest.raises(ValueError) as exc_info:
                YoutubeCaptionsFetcher.call(self.video_id, self.language)

        assert str(
            exc_info.value) == f"No manual captions found for video ID {self.video_id} and language {self.language}"
