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
            executor.submit(app.process_resource,
                            app.resource_message_to_json(msg))


def config_logs():
    logFilePath = f"log/{os.environ['SPEECH_ENV']}.log"
    logFormatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    root = logging.getLogger()

    for logging_level in [logging.ERROR, logging.INFO]:
        root.setLevel(logging_level)
        for handler in [logging.FileHandler(logFilePath), logging.StreamHandler(sys.stdout)]:
            handler.setLevel(logging_level)
            handler.setFormatter(logFormatter)
            root.addHandler(handler)


if __name__ == '__main__':
    main()
