from app import InputItemTiktok
from TikTokAPI import TikTokAPI
import app
import concurrent.futures
import glob
from unittest import mock
import os
import pytest
import re

tiktok_ids = ['7107586262877375746', '7105531486224370946']


class TestInputItemTiktok:
    def teardown_method(self):
        for fname in glob.glob('resources/multimedia/test/*.mp4'):
            os.remove(fname)

    @pytest.fixture
    @mock.patch.dict(os.environ, {'TIKTOK_COOKIE_S_V_WEB_ID': 'EXAMPLE-A'})
    @mock.patch.dict(os.environ, {'TIKTOK_COOKIE_TT_WEBID': 'EXAMPLE-B'})
    def api(self):
        cookie = app.tiktok_cookie_configured()
        api = TikTokAPI(cookie)
        api.downloadVideoById = mock.Mock()
        return api

    def test_save_simple(self):
        input_item = InputItemTiktok(
            resource_id=42, language_code='en', id=tiktok_ids[0])
        filepath = input_item.save()
        assert re.match(r'^' + re.escape(os.getcwd()) +
                        r'/resources/multimedia/test/\d+-42-\d{2}-\d{2}\.\d{2}:\d{2}:\d+\.mp4$', filepath)
        assert os.path.exists(filepath)

    def test_save_with_threads(self):
        filepaths = []
        with concurrent.futures.ThreadPoolExecutor(len(tiktok_ids)) as executor:
            for id in tiktok_ids:
                executor.submit(lambda id:
                                filepaths.append(
                                    InputItemTiktok(id=id, language_code='en',
                                                    resource_id=42).save()
                                ), id)
        for path in filepaths:
            assert os.path.exists(path)
