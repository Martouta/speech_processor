#!/bin/bash

exit_code=0

cd "$( dirname "${BASH_SOURCE[0]}" )"
cd '..'

echo "
********************************************************************************
*** Running Tests for SpeechProcessor
********************************************************************************"

MONGO_DB=speech_processor_test KAFKA_RESOURCE_TOPIC=speech_processor_resource_test SPEECH_ENV=test python3 -m pytest tests --tb=native -rP
((exit_code+=$?))

exit $exit_code
