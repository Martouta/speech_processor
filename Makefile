# Run all tests after running MongoDB and Kafka (Zookeeper). Run dependent services inside Docker containers and the tests locally (not inside a Docker container, but in the host instead).
test:
	docker compose up -d mongodb kafka
	./scripts/test.sh

# Process the fixture example_input as input and set the output in a file. In development environment. Run locally (not inside a Docker container, but in the host instead).
process:
	MAX_THREADS=8 INPUT_FILE='tests/fixtures/example_input.json' SPEECH_ENV='development' SUBS_LOCATION='file' python3 .
