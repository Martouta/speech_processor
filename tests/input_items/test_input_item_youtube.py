from cmath import exp
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
        filepath = self.submit_save_request(youtube_ids[0])
        expected_filepath_regexp = r'^' + re.escape(f"{os.getcwd()}/") \
            + re.escape('resources/multimedia/test/') \
            + r'\d+-55-' \
            + r'\d{2}-\d{2}\.\d{2}:\d{2}:\d+\.mp4$'
        assert re.match(expected_filepath_regexp, filepath)
        assert os.path.exists(filepath)

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    def test_save_with_threads(self):
        with concurrent.futures.ThreadPoolExecutor(len(youtube_ids)) as executor:
            for id in youtube_ids:
                executor.submit(self.submit_save_request, id)
        filepaths = glob.glob('resources/multimedia/test/*55*.mp4')
        assert len(filepaths) == 2

    def submit_save_request(self, id):
        item = InputItemYoutube(id=id, language_code='en', resource_id=55)
        return item.save()

    def test_download_params(self):
        filepath = f"{os.getcwd()}/tests/fixtures/example.mp4"
        params = InputItemYoutube.downloads_params(filepath)
        expected_params = {
            'output_path': f"{os.getcwd()}/tests/fixtures",
            'filename': 'example.mp4'}
        assert params == expected_params
