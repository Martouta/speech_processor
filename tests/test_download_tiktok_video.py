import app
import concurrent.futures
import pytest
import os

tiktok_ids = ['7107586262877375746', '7105531486224370946']


class TestDownloadTiktokVideo:
    def teardown_method(self):
        for filename in tiktok_ids:
            path = f"{os.getcwd()}/videos/test/download-tiktok-{filename}.mp4"
            if os.path.exists(path):
                os.remove(path)

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_download_tiktok_video_simple(self):
        path_tuple = ('videos/test', f"download-tiktok-{tiktok_ids[0]}.mp4")
        app.download_tiktok_video(tiktok_ids[0], path_tuple)
        assert os.path.exists(f"{path_tuple[0]}/{path_tuple[1]}")

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_download_tiktok_video_with_threads(self):
        with concurrent.futures.ThreadPoolExecutor(len(tiktok_ids)) as executor:
            for filename in tiktok_ids:
                app.download_tiktok_video(filename, (f"{os.getcwd()}/videos/test", f"download-tiktok-{filename}.mp4"))
        for filename in tiktok_ids:
            path = f"{os.getcwd()}/videos/test/download-tiktok-{filename}.mp4"
            assert os.path.exists(path)