from app import InputItemHosted
import glob
import os
import re
import requests_mock


class TestInputItemHosted:
    def teardown_method(self):
        for fname in glob.glob('resources/multimedia/test/*.mp4'):
            os.remove(fname)

    def test_save(self):
        web_root_uri = 'http://localhost:3000'
        url = f"{web_root_uri}/example.mp4"
        filepath = None
        with requests_mock.Mocker() as req_mock:
            req_mock.get(url, json={"a": "b"})
            input_item = InputItemHosted(
                resource_id=42, language_code='ar', url=url, extension='mp4')
            filepath = input_item.save()
        assert re.match(r'^' + re.escape(os.getcwd()) +
                        r'/resources/multimedia/test/\d+-42-\d{2}-\d{2}\.\d{2}:\d{2}:\d+\.mp4$', filepath)
        with open(filepath, 'r') as file:
            assert file.read().replace('\n', '') == '{"a": "b"}'
