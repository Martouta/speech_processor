import app
import os
import pytest
import kafka


class TestKafkaConsumerConfigured:
    @pytest.mark.skipif(os.getenv('CIRCLECI', '0') != '0', reason="Kafka")
    def test_kafka_consumer_configured(self):
        config = app.kafka_consumer_configured()
        # Not raising an error means that it could connect
        assert type(config) == kafka.consumer.group.KafkaConsumer
