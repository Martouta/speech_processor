import app
import builtins
import pytest
import os
import requests
import requests_mock


class TestDownloadMultimedia:
    def teardown_method(self):
        for resource_type in ['audios', 'videos']:
            for extension in ['mp3', 'mp4', 'example']:
                path = f"{os.getcwd()}/{resource_type}/test/recognition_id-example.{extension}"
                if os.path.exists(path):
                    os.remove(path)
        for path in [f"{os.getcwd()}/videos/recognition_id-zWQJqt_D-vo.mp4", f"{os.getcwd()}/videos/test/recognition_id-7105531486224370946.mp4"]:
            if os.path.exists(path):
                os.remove(path)

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_download_multimedia_for_youtube(self):
        actual_path = app.download_multimedia(
            'recognition_id', {'id': 1, 'youtube_reference_id': 'zWQJqt_D-vo'})
        expected_path = f"{os.getcwd()}/audios/test/recognition_id-zWQJqt_D-vo.mp4"
        assert actual_path == expected_path

    def test_download_multimedia_for_tiktok(self):
        actual_path = app.download_multimedia(
            'recognition_id', {'id': 1, 'tiktok_reference_id': '7105531486224370946'})
        expected_path = f"{os.getcwd()}/videos/test/recognition_id-7105531486224370946.mp4"
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

    def method_params(self, video_url='', audio_url='', filename='example', extension='example'):
        return {
            'id': 1,
            'video': {'url': video_url, 'filename': filename, 'extension': extension},
            'audio': {'url': audio_url, 'filename': filename, 'extension': extension}
        }
