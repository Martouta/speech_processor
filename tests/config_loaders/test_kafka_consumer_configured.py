from app.config_loaders.kafka_consumer_configured import kafka_consumer_configured
import kafka


class TestKafkaConsumerConfigured:
    def test_kafka_consumer_configured(self):
        config = kafka_consumer_configured()
        # Not raising an error means that it could connect
        assert type(config) == kafka.consumer.group.KafkaConsumer
