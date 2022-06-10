import pytest
import app
import os
from unittest import mock


class TestTiktokCookieConfigured:
    @mock.patch.dict(os.environ, {'TIKTOK_COOKIE_S_V_WEB_ID': 'EXAMPLE-A'})
    def test_tiktok_cookie_configured(self):
        config = app.tiktok_cookie_configured()
        assert config['s_v_web_id'] == 'EXAMPLE-A'
