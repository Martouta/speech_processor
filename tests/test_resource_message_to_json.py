import pytest
import app
import json
from kafka.protocol.message import Message

class TestResourceMessageToJSON:

    def test_dict_unwrapped_resource_message_to_json(self):
        message = self.unwrapped_resource_message()
        response = app.resource_message_to_json(message)
        assert response == self.unwrapped_resource_message()

    def test_dict_wrapped_resource_message_to_json(self):
        message = self.wrapped_resource_message()
        response = app.resource_message_to_json(message)
        assert response == self.unwrapped_resource_message()

    def test_kafka_unwrapped_resource_message_to_json(self):
        message = Message(json.dumps(self.unwrapped_resource_message()).encode('ascii'), key=b'key')
        response = app.resource_message_to_json(message)
        assert response == self.unwrapped_resource_message()

    def test_kafka_wrapped_resource_message_to_json(self):
        message = Message(value=json.dumps(self.wrapped_resource_message()).encode('ascii'), key=b'key')
        response = app.resource_message_to_json(message)
        assert response == self.unwrapped_resource_message()

    def unwrapped_resource_message(self):
        return {
            'type': 'youtube',
            'id': 'zWQJqt_D-vo',
            'resource_id': 1,
            'language_code': 'ar'
        }

    def wrapped_resource_message(self):
        return {
            'resource': self.unwrapped_resource_message()
        }
