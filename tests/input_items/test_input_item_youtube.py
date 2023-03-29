from cmath import exp
from app import InputItemYoutube
import concurrent.futures
import glob
import os
from app.input_items.recognizer_data import RecognizerData
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
        item = InputItemYoutube(id=id, recognizer_data=RecognizerData(
            language_code='en'), resource_id=55)
        return item.save()

    def test_download_params(self):
        filepath = f"{os.getcwd()}/tests/fixtures/example.mp4"
        params = InputItemYoutube.downloads_params(filepath)
        expected_params = {
            'output_path': f"{os.getcwd()}/tests/fixtures",
            'filename': 'example.mp4'}
        assert params == expected_params

    def test_are_captions_requested(self):
        recognizer_data = RecognizerData(language_code='en')
        item_without_captions = InputItemYoutube(
            id=youtube_ids[0], recognizer_data=recognizer_data, resource_id=55)
        assert not item_without_captions.are_captions_requested()

        recognizer_data = RecognizerData(language_code='en', captions=True)
        item_with_captions = InputItemYoutube(
            id=youtube_ids[0], recognizer_data=recognizer_data, resource_id=55)
        assert item_with_captions.are_captions_requested()
