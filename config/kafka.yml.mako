<%!
    import os
    def kafka_brokers():
        return os.getenv('KAFKA_URL', 'localhost:9092')

    def kafka_topic():
        return os.environ['KAFKA_RESOURCE_TOPIC']
%>

development:
  topic_publish_resource: ${ kafka_topic() }
  brokers: ${ kafka_brokers() }

production:
  topic_publish_resource: ${ kafka_topic() }
  brokers: ${ kafka_brokers() }

test:
  topic_publish_resource: ${ kafka_topic() }
  brokers: ${ kafka_brokers() }
