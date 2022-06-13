import pytest
import app
import os
from unittest import mock


class TestFetchInputMessages:
    INPUT_FILE = f"{os.getcwd()}/tests/fixtures/example_input.json"

    @mock.patch.dict(os.environ, {'INPUT_FILE': INPUT_FILE})
    def test_fetch_input_msgs_from_input_file(self):
        messages = app.fetch_input_messages()
        assert messages == app.json_input_resources(TestFetchInputMessages.INPUT_FILE)

    def test_fetch_input_msgs_from_kafka(self):
        messages = app.fetch_input_messages()
        assert type(messages) == type(app.kafka_consumer_configured())
