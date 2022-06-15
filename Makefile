# Run all tests after running MongoDB and Kafka (Zookeeper). Run dependent services inside Docker containers and the tests locally (not inside a Docker container, but in the host instead).
test_host:
	docker compose up -d mongodb kafka
	./scripts/test.sh

# Run all tests after running MongoDB and Kafka (Zookeeper). Run everything inside Docker.
test_docker:
	docker compose up -d
	docker compose logs --timestamps --follow speech_processor_test

# Process the fixture example_input as input and set the output in a file. In development environment. Run locally (not inside a Docker container, but in the host instead).
process:
	MAX_THREADS=8 INPUT_FILE='tests/fixtures/example_input.json' SPEECH_ENV='development' SUBS_LOCATION='file' python3 .

# Remove all folders and files like: .pyc, .pyo, __pycache__ and pytest_cache.
clear_cache:
	find . | grep -E '__pycache__|\.pyc|\.pyo|\.pytest_cache' | xargs rm -rf
