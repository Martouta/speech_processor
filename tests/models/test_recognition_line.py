from app.models.duration import Duration
from app.models.recognition_line import RecognitionLine


class TestRecognitionLine:
    def setup_method(self):
        self.line = RecognitionLine("Hello, world!", Duration(0, 10))

    def test_eq_same_object(self):
        assert self.line == self.line

    def test_eq_different_objects_same_values(self):
        other_line = RecognitionLine("Hello, world!", Duration(0, 10))
        assert self.line == other_line

    def test_eq_different_objects_different_text(self):
        other_line = RecognitionLine("Goodbye, world!", Duration(0, 10))
        assert self.line != other_line

    def test_eq_different_objects_different_duration(self):
        other_line = RecognitionLine("Hello, world!", Duration(1, 11))
        assert self.line != other_line

    def test_eq_different_objects_different_text_and_duration(self):
        other_line = RecognitionLine("Goodbye, world!", Duration(1, 11))
        assert self.line != other_line

    def test_eq_different_object_types(self):
        assert self.line != "Hello, world!"
        assert self.line != Duration(0, 10)
        assert self.line != 42

    def test_init(self):
        assert self.line.text == "Hello, world!"
        assert self.line.duration == Duration(0, 10)

    def test_str(self):
        assert str(self.line) == "00:00:00,000;00:00:00,010;Hello, world!"

    def test_repr(self):
        assert repr(self.line) == "RecognitionLine(text='Hello, world!', duration=Duration(ts_start=0, ts_end=10))"

    def test_duration_ts_start_srt(self):
        assert self.line.duration_ts_start_srt() == "00:00:00,000"

    def test_duration_ts_end_srt(self):
        assert self.line.duration_ts_end_srt() == "00:00:00,010"

    def test_duration_ts_srt(self):
        assert self.line.duration_ts_srt() == "00:00:00,000 --> 00:00:00,010"

    def test_to_dict(self):
        expected_dict = {
            'timestamp': '00:00:00,000 --> 00:00:00,010',
            'text': 'Hello, world!'
        }
        assert self.line.to_dict() == expected_dict
