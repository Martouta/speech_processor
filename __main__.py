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


def config_logs():
    speech_env = os.environ['SPEECH_ENV']
    logFilePath = f"log/{speech_env}.log"
    logFormatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    root = logging.getLogger()

    handler_collection = [logging.FileHandler(logFilePath)]
    if speech_env != 'test':
        handler_collection.append(logging.StreamHandler(sys.stdout))

    for logging_level in [logging.ERROR, logging.INFO]:
        root.setLevel(logging_level)
        for handler in handler_collection:
            handler.setLevel(logging_level)
            handler.setFormatter(logFormatter)
            root.addHandler(handler)


if __name__ == '__main__':
    main()
