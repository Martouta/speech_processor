import glob
import os
import re
from app.input_items.input_item_local import InputItemLocal
from app.input_items.recognizer_data import RecognizerData


class TestInputItemLocal:
    def teardown_method(self):
        for fname in glob.glob('resources/multimedia/test/example.txt'):
            os.remove(fname)

    def test_save(self):
        item = InputItemLocal(
            resource_id=42, path='tests/fixtures/example.txt', recognizer_data=RecognizerData(language_code='en')
        )
        filepath = item.save()

        assert re.match(r'^' + re.escape(os.getcwd()) +
                        r'/resources/multimedia/test/\d+-42-\d{2}-\d{2}\.\d{2}:\d{2}:\d+\.txt$', filepath)
        with open(filepath, 'r') as file:
            assert file.read().replace('\n', '') == 'Hello, World!'
