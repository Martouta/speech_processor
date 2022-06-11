import app
import concurrent.futures
import pytest
import os

youtube_ids = ['zWQJqt_D-vo', '2_qNGoE315M']


class TestDownloadYoutubeVideo:
    def teardown_method(self):
        for filename in youtube_ids:
            path = f"{os.getcwd()}/videos/test/download-youtube-{filename}.mp4"
            if os.path.exists(path):
                os.remove(path)

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_download_youtube_video_simple(self):
        path_tuple = ('videos/test', f"download-youtube-{youtube_ids[0]}.mp4")
        app.download_youtube_video(youtube_ids[0], path_tuple)
        assert os.path.exists(f"{path_tuple[0]}/{path_tuple[1]}")

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_download_youtube_video_with_threads(self):
        with concurrent.futures.ThreadPoolExecutor(len(youtube_ids)) as executor:
            for filename in youtube_ids:
                app.download_youtube_video(filename, (f"{os.getcwd()}/videos/test", f"download-youtube-{filename}.mp4"))
        for filename in youtube_ids:
            path = f"{os.getcwd()}/videos/test/download-youtube-{filename}.mp4"
            assert os.path.exists(path)
