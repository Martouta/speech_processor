import app
import concurrent.futures
import pytest
import os

tiktok_ids = ['7107586262877375746', '7105531486224370946']


class TestDownloadTiktokVideo:
    def teardown_method(self):
        for filename in tiktok_ids:
            path = f"{os.getcwd()}/resources/multimedia/test/download-tiktok-{id}.mp4"
            if os.path.exists(path):
                os.remove(path)

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_download_tiktok_video_simple(self):
        app.download_tiktok_video(
            tiktok_ids[0], 'resources/multimedia/test', f"download-tiktok-{tiktok_ids[0]}.mp4")
        assert os.path.exists(
            f"resources/multimedia/test/download-tiktok-{tiktok_ids[0]}.mp4")

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_download_tiktok_video_with_threads(self):
        with concurrent.futures.ThreadPoolExecutor(len(tiktok_ids)) as executor:
            for id in tiktok_ids:
                app.download_tiktok_video(
                    id, f"{os.getcwd()}/resources/multimedia/test", f"download-tiktok-{id}.mp4")
        for id in tiktok_ids:
            path = f"{os.getcwd()}/resources/multimedia/test/download-tiktok-{id}.mp4"
            assert os.path.exists(path)
