from app import Duration
import re
import os


class TestDuration:
    FILEPATH = f"{os.getcwd()}/resources/audio_chunks/test/test_duration.txt"

    def setup_method(self):
        self.duration = Duration(1000, 2000)

    def teardown_method(self):
        if os.path.exists(TestDuration.FILEPATH):
            os.remove(TestDuration.FILEPATH)

    def test_str(self):
        expected_output = """<class 'app.models.duration.Duration'>
                            ts_start = 00:00:01,000
                            ts_end = 00:00:02,000
                            """
        expected_output = re.sub(r'[ \t]{2,}', '', expected_output)
        assert str(self.duration) == expected_output

    def test_duration_equality(self):
        duration1 = Duration(ts_start=10, ts_end=20)
        duration2 = Duration(ts_start=10, ts_end=20)
        duration3 = Duration(ts_start=20, ts_end=30)
        assert duration1 == duration2
        assert duration1 != duration3
        assert duration1 != '00:00:01,000;00:00:02,000'

    def test_srt_methods(self):
        assert self.duration.ts_start_srt() == "00:00:01,000"
        assert self.duration.ts_end_srt() == "00:00:02,000"

    def test_export(self):
        index = 1
        self.duration.export(TestDuration.FILEPATH, index)
        with open(TestDuration.FILEPATH, 'r') as file:
            assert file.read() == "1;00:00:01,000;00:00:02,000"

    def test_duration_from_srt(self):
        start = '00:00:01,500'
        end = '00:00:03,000'
        duration = Duration.from_srt(start, end)
        assert duration.ts_start == 1500
        assert duration.ts_end == 3000

    def test_ms_srt_conversions(self):
        srt_timestamp = "00:00:01,000"
        ms = 1000
        assert Duration.ms_to_srt_timestamp(ms) == srt_timestamp
        assert Duration.srt_timestamp_to_ms(srt_timestamp) == ms
