from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import mock_open, patch
import pytest

import healthcheck
from healthcheck import get_last_log_line, is_liveness_ok, is_readiness_ok


class TestHealthCheck:
    def test_get_last_log_line(self):
        with patch("builtins.open", mock_open(read_data="log line 1\nlog line 2\n")):
            assert get_last_log_line() == "log line 2\n"

    def test_is_liveness_ok_returns_false_if_no_log_line(self):
        assert not is_liveness_ok(None)

    def test_is_liveness_ok_returns_false_if_last_log_line_is_an_error_older_than_liveness_threshold(self):
        with patch.object(healthcheck, 'LIVENESS_THRESHOLD', timedelta(seconds=5)):
            liveness_threshold = timedelta(seconds=5)
            now = datetime.now()
            log_line = f"{now - liveness_threshold - timedelta(seconds=1)} - ERROR - test message\n"

            assert not is_liveness_ok(log_line)

    def test_is_liveness_ok_returns_true_if_last_log_line_is_an_error_younger_than_liveness_threshold(
        self,
    ):
        liveness_threshold = timedelta(minutes=5)
        log_line = f"{datetime.now() - liveness_threshold + timedelta(seconds=1)} - ERROR - test message\n"
        assert is_liveness_ok(log_line)

    def test_is_liveness_ok_returns_true_if_last_log_line_is_not_an_error(self):
        log_line = f"{datetime.now()} - INFO - test message\n"
        assert is_liveness_ok(log_line)

    def test_is_readiness_ok_returns_false_if_log_line_does_not_contain_connection_to_kafka_established(
        self,
    ):
        log_line = "log message without the expected substring\n"
        assert not is_readiness_ok(log_line)

    def test_is_readiness_ok_returns_true_if_log_line_contains_connection_to_kafka_established(self):
        log_line = "Connection to kafka established\n"
        assert is_readiness_ok(log_line)

    @patch('healthcheck.os.environ', {"SPEECH_ENV": "test", "PROBE_TYPE": "liveness"})
    @patch('healthcheck.get_last_log_line')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_liveness_ok(self, mock_stdout, mock_get_last_log_line):
        mock_get_last_log_line.return_value = f"{datetime.now()} - INFO - test message\n"
        with pytest.raises(SystemExit) as exc_info:
            healthcheck.main()
        assert exc_info.value.code == 0
        assert mock_stdout.getvalue() == "OK\n"

    @patch('healthcheck.os.environ', {"SPEECH_ENV": "test", "PROBE_TYPE": "readiness"})
    @patch('healthcheck.get_last_log_line')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_readiness_ok(self, mock_stdout, mock_get_last_log_line):
        mock_get_last_log_line.return_value = "Connection to kafka established\n"
        with pytest.raises(SystemExit) as exc_info:
            healthcheck.main()
        assert exc_info.value.code == 0
        assert mock_stdout.getvalue() == "OK\n"

    @patch('healthcheck.os.environ', {"SPEECH_ENV": "test", "PROBE_TYPE": "unknown"})
    @patch('healthcheck.get_last_log_line')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_unknown_probe_type(self, mock_stdout, mock_get_last_log_line):
        mock_get_last_log_line.return_value = f"{datetime.now()} - INFO - test message\n"
        with pytest.raises(SystemExit) as exc_info:
            healthcheck.main()
        assert exc_info.value.code == 1
        assert mock_stdout.getvalue() == "Unknown probe type\n"
