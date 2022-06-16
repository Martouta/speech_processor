# Run all tests after running MongoDB and Kafka (with Zookeeper). Run dependent services inside Docker containers and the tests locally (not inside a Docker container, but in the host instead).
test_host:
	docker-compose up -d mongodb kafka
	./scripts/test.sh

# Run all tests after running MongoDB and Kafka (with Zookeeper). Run everything inside Docker.
test_docker:
	docker-compose up -d
	docker-compose logs --timestamps --follow speech_processor_test

# Run a docker container (bash) with this project and in the background (connected) Kafka (with Zookeeper) and MongoDB.
development_docker:
	docker-compose up -d mongodb kafka
	docker-compose run -i -t speech_processor_development /bin/bash

# Process the fixture example_input as input and set the output in a file. In development environment. Run locally (not inside a Docker container, but in the host instead).
process:
	MAX_THREADS=8 INPUT_FILE='tests/fixtures/example_input.json' SPEECH_ENV='development' SUBS_LOCATION='file' python3 .

# Remove all folders and files like: .pyc, .pyo, __pycache__ and pytest_cache.
clear_cache:
	find . | grep -E '__pycache__|\.pyc|\.pyo|\.pytest_cache' | xargs rm -rf

# Deploy to production. Call like: make version=example deploy_production
# It builds the docker image, pushes it to dockerhub, created the github release and tag remotely and locally, and finally, it sets the new image to production (k8s).
deploy_production:
	docker build -t martouta/speech_processor:$(version) -f Dockerfile.production .
	docker push martouta/speech_processor:$(version)
	gh release create $(version) --title "$(version)" --notes "Release generated with 'make version=$(version) deploy_production'"
	git fetch -t
	kubectl set image deployment speech-processor speech-processor=martouta/speech_processor:$(version)
