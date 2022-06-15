from app import InputItemYoutube
import concurrent.futures
import glob
import os
import pytest
import re

youtube_ids = ['zWQJqt_D-vo', '2_qNGoE315M']


class TestInputItemYoutube:
    def teardown_method(self):
        for fname in glob.glob('resources/multimedia/test/*.mp4'):
            os.remove(fname)

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_save_simple(self):
        input_item = InputItemYoutube(
            id=youtube_ids[0], language_code='en', resource_id=42)
        filepath = input_item.save()
        assert re.match(r'^' + re.escape(os.getcwd()) +
                        r'/resources/multimedia/test/\d+-42-\d{2}-\d{2}\.\d{2}:\d{2}:\d+\.mp4$', filepath)
        assert os.path.exists(filepath)

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_save_with_threads(self):
        filepaths = []
        with concurrent.futures.ThreadPoolExecutor(len(youtube_ids)) as executor:
            for id in youtube_ids:
                input_item = InputItemYoutube(
                    id=youtube_ids[0], language_code='en', resource_id=42)
                path = input_item.save()
                filepaths.append(path)
        for path in filepaths:
            assert os.path.exists(path)
