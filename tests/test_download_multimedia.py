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

    def test_download_multimedia_for_video(self):
        self.correct_download_multimedia('example.mp4', '')

    def test_download_multimedia_for_audio(self):
        self.correct_download_multimedia('', 'example.mp3')

    def test_download_multimedia_for_video_and_audio(self):
        self.correct_download_multimedia('example.mp4', 'example.mp3')

    def correct_download_multimedia(self, video_path, audio_path):
        web_root_uri = 'http://localhost:3000'
        video_url = f"{web_root_uri}/{video_path}"
        audio_url = f"{web_root_uri}/{audio_path}"
        with requests_mock.Mocker() as req_mock:
            req_mock.get(video_url, json={"a": "b"})
            req_mock.get(audio_url, json={"a": "b"})
            filepath = app.download_multimedia(
                'recognition_id', self.method_params(video_url=video_url, audio_url=audio_url))
            with open(filepath, 'r') as file:
                assert file.read().replace('\n', '') == '{"a": "b"}'

    def method_params(self, video_url=None, audio_url=None, filename='example', extension='example'):
        resource_type = 'hosted_audio'
        if video_url:
            resource_type = 'hosted_video'

        return {
            'type': resource_type,
            'resource_id': 1,
            'url': video_url or audio_url or '',
            'filename': filename,
            'extension': extension
        }
