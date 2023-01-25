from app import RecognitionLine
from app import Duration


class TestRecognitionLine:
    def setup_method(self):
        self.line = RecognitionLine("Hello, world!", Duration(0, 10))

    def test_init(self):
        assert self.line.text == "Hello, world!"
        assert self.line.duration == Duration(0, 10)

    def test_str(self):
        assert str(self.line) == "00:00:00,000;00:00:00,010;Hello, world!"

    def test_duration_ts_start_srt(self):
        assert self.line.duration_ts_start_srt() == "00:00:00,000"

    def test_duration_ts_end_srt(self):
        assert self.line.duration_ts_end_srt() == "00:00:00,010"