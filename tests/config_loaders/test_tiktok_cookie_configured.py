import os
from unittest import mock
from app.config_loaders.tiktok_cookie_configured import tiktok_cookie_configured


class TestTiktokCookieConfigured:
    @mock.patch.dict(os.environ, {'TIKTOK_COOKIE_S_V_WEB_ID': 'EXAMPLE-A'})
    @mock.patch.dict(os.environ, {'TIKTOK_COOKIE_TT_WEBID': 'EXAMPLE-B'})
    def test_tiktok_cookie_configured(self):
        config = tiktok_cookie_configured()
        assert config['s_v_web_id'] == 'EXAMPLE-A'
        assert config['tt_webid'] == 'EXAMPLE-B'
