from TikTokAPI import TikTokAPI
from ..config_loaders.tiktok_cookie_configured import tiktok_cookie_configured
from .input_item import InputItem


class InputItemTiktok(InputItem):
    def __init__(self, *, resource_id, language_code, id):
        super().__init__(resource_id=resource_id, language_code=language_code)
        self.id = id
        self.extension = 'mp4'

    def download(self, filepath):
        cookie = tiktok_cookie_configured()
        api = TikTokAPI(cookie)
        api.downloadVideoById(self.id, filepath)
