import app
import concurrent.futures
import json
import logging
import os
import sys


def main() -> None:
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

    max_workers = int(os.getenv('MAX_THREADS', '5'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        input_messages = []
        if os.getenv('INPUT_FILE'):
            input_messages = app.json_input_resources(os.getenv('INPUT_FILE'))
            for msg in input_messages:
                executor.submit(app.process_resource, msg)
        else:
            input_messages = app.kafka_consumer_configured()
            for msg in input_messages:
                executor.submit(app.process_resource, json.loads(msg.value))


if __name__ == '__main__':
    main()
