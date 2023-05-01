import app
import concurrent.futures
import os


def main() -> None:
    log_output = os.environ.get('LOG_OUTPUT', 'file')
    log_configurator = app.LogConfigurator(log_output)
    log_configurator.configure_logging()
    process_threaded_inputs()


def process_threaded_inputs():
    max_workers = int(os.getenv('MAX_THREADS', '5'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for msg in app.fetch_input_messages():
            executor.submit(app.process_resource, msg)


if __name__ == '__main__':
    main()
