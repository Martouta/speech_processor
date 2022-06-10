IMAGE_NAME = testing

all: build run

build: Dockerfile
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm -i -t $(IMAGE_NAME) /bin/bash
