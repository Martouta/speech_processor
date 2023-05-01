import logging
import os
import sys


class LogConfigurator:
    def __init__(self, log_output='file'):
        self.log_output = log_output

    def configure_logging(self):
        logFormatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        if self.log_output in ['file', 'both']:
            file_handler = self._create_file_handler()
            self._configure_handler(file_handler, logFormatter, root)

        if self.log_output in ['standard', 'both']:
            stdout_handler, stderr_handler = self._create_standard_handlers()
            self._configure_handler(stdout_handler, logFormatter, root)
            self._configure_handler(stderr_handler, logFormatter, root)

    def _create_file_handler(self):
        logFilePath = f"log/{os.environ['SPEECH_ENV']}.log"
        return logging.FileHandler(logFilePath)

    def _create_standard_handlers(self):
        stdout_handler = logging.StreamHandler(sys.stdout)
        stderr_handler = logging.StreamHandler(sys.stderr)
        return stdout_handler, stderr_handler

    def _configure_handler(self, handler, logFormatter, root):
        handler.setFormatter(logFormatter)
        root.addHandler(handler)
