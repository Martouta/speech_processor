import app
import concurrent.futures
import logging
import os
import sys


def main() -> None:
    config_logs()
    process_threaded_inputs()


def process_threaded_inputs():
    max_workers = int(os.getenv('MAX_THREADS', '5'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for msg in app.fetch_input_messages():
            executor.submit(app.process_resource, msg)


def create_file_handler(logFilePath):
    file_handler = logging.FileHandler(logFilePath)
    return file_handler


def create_standard_handlers():
    stdout_handler = logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)
    return stdout_handler, stderr_handler


def set_handler_level(handler, level, filter_func=None):
    handler.setLevel(level)
    if filter_func:
        handler.addFilter(filter_func)


def configure_handler(handler, log_output, logFormatter, root, stdout_handler=None, stderr_handler=None):
    handler.setFormatter(logFormatter)
    root.addHandler(handler)

    if log_output in ['standard', 'both']:
        if handler is stdout_handler:
            set_handler_level(handler, logging.INFO,
                              lambda record: record.levelno <= logging.INFO)
        elif handler is stderr_handler:
            set_handler_level(handler, logging.ERROR)
    else:
        set_handler_level(handler, logging.INFO)


def config_logs():
    speech_env = os.environ['SPEECH_ENV']
    log_output = os.environ.get('LOG_OUTPUT', 'file')
    logFilePath = f"log/{speech_env}.log"
    logFormatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    root = logging.getLogger()

    root.setLevel(logging.INFO)

    if log_output in ['file', 'both']:
        file_handler = create_file_handler(logFilePath)
        configure_handler(file_handler, log_output, logFormatter, root)

    if log_output in ['standard', 'both']:
        stdout_handler, stderr_handler = create_standard_handlers()
        configure_handler(stdout_handler, log_output, logFormatter, root,
                          stdout_handler=stdout_handler, stderr_handler=stderr_handler)
        configure_handler(stderr_handler, log_output, logFormatter, root,
                          stdout_handler=stdout_handler, stderr_handler=stderr_handler)


if __name__ == '__main__':
    main()
