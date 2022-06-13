import app
import pytest
import os
import requests_mock


class TestDownloadMultimedia:
    def teardown_method(self):
        for extension in ['mp3', 'mp4', 'example']:
            for filename in ['recognition_id-example', 'recognition_id-zWQJqt_D-vo', 'recognition_id-7105531486224370946']:
                path = f"{os.getcwd()}/resources/multimedia/test/{filename}.{extension}"
                if os.path.exists(path):
                    os.remove(path)

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_download_multimedia_for_youtube(self):
        actual_path = app.download_multimedia(
            'recognition_id', {'resource_id': 1, 'id': 'zWQJqt_D-vo', 'type': 'youtube'})
        expected_path = f"{os.getcwd()}/resources/multimedia/test/recognition_id-zWQJqt_D-vo.mp4"
        assert actual_path == expected_path

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_download_multimedia_for_tiktok(self):
        actual_path = app.download_multimedia(
            'recognition_id', {'resource_id': 1, 'id': '7105531486224370946', 'type': 'tiktok'})
        expected_path = f"{os.getcwd()}/resources/multimedia/test/recognition_id-7105531486224370946.mp4"
        assert actual_path == expected_path

    def test_download_multimedia_for_hosted(self):
        web_root_uri = 'http://localhost:3000'
        url = f"{web_root_uri}/example.mp4"
        with requests_mock.Mocker() as req_mock:
            req_mock.get(url, json={"a": "b"})
            filepath = app.download_multimedia(
                'recognition_id',
                {
                    'type': 'hosted',
                    'resource_id': 1,
                    'url': url,
                    'extension': 'mp4'
                })
            with open(filepath, 'r') as file:
                assert file.read().replace('\n', '') == '{"a": "b"}'
