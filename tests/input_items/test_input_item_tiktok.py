from app import InputItemTiktok
import concurrent.futures
import glob
import os
import pytest
import re

tiktok_ids = ['7107586262877375746', '7105531486224370946']


class TestInputItemTiktok:
    def teardown_method(self):
        for fname in glob.glob('resources/multimedia/test/*.mp4'):
            os.remove(fname)

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    @pytest.mark.filterwarnings('ignore::DeprecationWarning')
    def test_save_simple(self):
        input_item = InputItemTiktok(
            id=tiktok_ids[0], language_code='en', resource_id=42)
        filepath = input_item.save()
        assert re.match(r'^' + re.escape(os.getcwd()) +
                        r'/resources/multimedia/test/\d+-42-\d{2}-\d{2}\.\d{2}:\d{2}:\d+\.mp4$', filepath)
        assert os.path.exists(filepath)

    @pytest.mark.skipif(os.getenv('CIRCLECI') is not None, reason="no idea how to mock these real HTTP requests")
    @pytest.mark.filterwarnings('ignore::DeprecationWarning')
    def test_save_with_threads(self):
        filepaths = []
        with concurrent.futures.ThreadPoolExecutor(len(tiktok_ids)) as executor:
            for id in tiktok_ids:
                input_item = InputItemTiktok(
                    id=tiktok_ids[0], language_code='en', resource_id=42)
                path = input_item.save()
                filepaths.append(path)
        for path in filepaths:
            assert os.path.exists(path)
