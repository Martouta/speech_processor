from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import mock_open, patch
import pytest

import healthcheck
from healthcheck import get_all_log_lines, is_startup_ok


class TestHealthCheck:
    def test_get_all_log_lines(self):
        with patch("builtins.open", mock_open(read_data="log line 1\nlog line 2\n")):
            assert get_all_log_lines() == ["log line 1\n", "log line 2\n"]

    def test_is_startup_ok_returns_false_if_log_lines_do_not_contain_fetching_input_messages(
        self,
    ):
        log_lines = ["log message without the expected substring\n"]
        assert not is_startup_ok(log_lines)

    def test_is_startup_ok_returns_true_if_log_lines_contain_fetching_input_messages(self):
        log_lines = ["Fetching input messages\n"]
        assert is_startup_ok(log_lines)

    @patch('healthcheck.os.environ', {"SPEECH_ENV": "test", "PROBE_TYPE": "startup"})
    @patch('healthcheck.get_all_log_lines')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_startup_ok(self, mock_stdout, mock_get_all_log_lines):
        mock_get_all_log_lines.return_value = ["Fetching input messages\n"]
        with pytest.raises(SystemExit) as exc_info:
            healthcheck.main()
        assert exc_info.value.code == 0
        assert mock_stdout.getvalue() == "OK\n"

    @patch('healthcheck.os.environ', {"SPEECH_ENV": "test", "PROBE_TYPE": "unknown"})
    @patch('healthcheck.get_all_log_lines')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_unknown_probe_type(self, mock_stdout, mock_get_all_log_lines):
        mock_get_all_log_lines.return_value = [
            f"{datetime.now()} - INFO - test message\n"]
        with pytest.raises(SystemExit) as exc_info:
            healthcheck.main()
        assert exc_info.value.code == 1
        assert mock_stdout.getvalue() == "Unknown probe type\n"
