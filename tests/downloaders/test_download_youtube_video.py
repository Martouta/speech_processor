import app
import concurrent.futures
import pytest
import os

youtube_ids = ['zWQJqt_D-vo', '2_qNGoE315M']


class TestDownloadYoutubeVideo:
    def teardown_method(self):
        for id in youtube_ids:
            path = f"{os.getcwd()}/resources/multimedia/test/download-youtube-{id}.mp4"
            if os.path.exists(path):
                os.remove(path)

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_download_youtube_video_simple(self):
        app.download_youtube_video(
            youtube_ids[0], 'resources/multimedia/test', f"download-youtube-{youtube_ids[0]}.mp4")
        assert os.path.exists(
            f"resources/multimedia/test/download-youtube-{youtube_ids[0]}.mp4")

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_download_youtube_video_with_threads(self):
        with concurrent.futures.ThreadPoolExecutor(len(youtube_ids)) as executor:
            for id in youtube_ids:
                app.download_youtube_video(
                    id, f"{os.getcwd()}/resources/multimedia/test", f"download-youtube-{id}.mp4")
        for id in youtube_ids:
            path = f"{os.getcwd()}/resources/multimedia/test/download-youtube-{id}.mp4"
            assert os.path.exists(path)
