import glob
import os
import re
from app.input_items.input_item_hosted import InputItemHosted
from app.input_items.recognizer_data import RecognizerData
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
            item = InputItemHosted(resource_id=42, recognizer_data=RecognizerData(language_code='en'), url=url)
            filepath = item.save()
        assert re.match(r'^' + re.escape(os.getcwd()) +
                        r'/resources/multimedia/test/\d+-42-\d{2}-\d{2}\.\d{2}:\d{2}:\d+\.mp4$', filepath)
        with open(filepath, 'r') as file:
            assert file.read().replace('\n', '') == '{"a": "b"}'

    def test_extension(self):
        web_root_uri = 'http://localhost:3000'
        fname = 'example'

        supported_extensions = ['mp4', 'mp3', 'wav']
        supported_extensions += [ext.upper() for ext in supported_extensions]
        for ext in supported_extensions:
            url = f"{web_root_uri}/{fname}.{ext}?foo=bar"
            item = InputItemHosted(resource_id=42, recognizer_data=RecognizerData(language_code='en'), url=url)
            assert item.extension_from_url() == ext
            assert item.extension == ext

        ext = 'mkv'
        url = f"{web_root_uri}/{fname}.{ext}?foo=bar"
        item = InputItemHosted(resource_id=42, recognizer_data=RecognizerData(language_code='en'), url=url)
        assert item.extension_from_url() == ''
        assert item.extension == ''

        url = f"{web_root_uri}/no-multimedia-attached"
        item = InputItemHosted(resource_id=42, recognizer_data=RecognizerData(language_code='en'), url=url)
        assert item.extension_from_url() == ''
        assert item.extension == ''
