#!/bin/bash

exit_code=0

if [ "$MONGO_URL" == "" ]; then
  MONGO_URL="localhost:27017"
fi

if [ "$KAFKA_URL" == "" ]; then
  KAFKA_URL="localhost:29092"
fi

echo "Waiting for MongoDB to start on '$MONGO_URL' ... ⏳"
mongo_url_nc_format=`tr ':' ' ' <<<$MONGO_URL`
while ! nc -zv $mongo_url_nc_format -w 5; do
  sleep 0.1
done
echo "MongoDB started"

kafka_url_nc_format=`tr ':' ' ' <<<$KAFKA_URL`
echo "Waiting for Kafka to start on '$KAFKA_URL' ... ⏳"
while ! nc -zv $kafka_url_nc_format -w 5; do
  sleep 0.1
done
if ! [ -f /.dockerenv ]; then
    grep -q -e 'KafkaServer id=\d\] started' <(docker-compose logs -f kafka)
fi
echo "Kafka started"

echo "Running Tests for SpeechProcessor ..."

KAFKA_RESOURCE_TOPIC=speech_processor_resource_test MONGO_DB=speech_processor_test SPEECH_ENV='test' python3 -m pytest tests --tb=native -rP
((exit_code+=$?))

exit $exit_code
