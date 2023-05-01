import logging
import sys
import pytest
from app.log_configurator import LogConfigurator


class TestLogConfigurator:
    @pytest.fixture(autouse=True)
    def setUp(self, caplog):
        caplog.set_level(logging.NOTSET)
        self.root_logger = logging.getLogger()

    def test_configure_logging_file(self):
        log_output = 'file'
        log_configurator = LogConfigurator(log_output)

        initial_handler_count = len(self.root_logger.handlers)

        log_configurator.configure_logging()

        handlers = self.root_logger.handlers
        added_handler_count = len(handlers) - initial_handler_count

        assert added_handler_count == 1
        assert isinstance(handlers[-1], logging.FileHandler)

    def test_configure_logging_standard(self):
        log_output = 'standard'
        log_configurator = LogConfigurator(log_output)

        initial_handler_count = len(self.root_logger.handlers)

        log_configurator.configure_logging()

        handlers = self.root_logger.handlers
        added_handler_count = len(handlers) - initial_handler_count

        assert added_handler_count == 2
        assert isinstance(handlers[-2], logging.StreamHandler)
        assert isinstance(handlers[-1], logging.StreamHandler)
        assert handlers[-2].stream == sys.stdout
        assert handlers[-1].stream == sys.stderr

    def test_configure_logging_both(self):
        log_output = 'both'
        log_configurator = LogConfigurator(log_output)

        initial_handler_count = len(self.root_logger.handlers)

        log_configurator.configure_logging()

        handlers = self.root_logger.handlers
        added_handler_count = len(handlers) - initial_handler_count

        assert added_handler_count == 3
        assert isinstance(handlers[-3], logging.FileHandler)
        assert isinstance(handlers[-2], logging.StreamHandler)
        assert isinstance(handlers[-1], logging.StreamHandler)
        assert handlers[-2].stream == sys.stdout
        assert handlers[-1].stream == sys.stderr
