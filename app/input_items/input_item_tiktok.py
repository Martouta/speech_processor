from TikTokAPI import TikTokAPI
from ..config_loaders.tiktok_cookie_configured import tiktok_cookie_configured
from .input_item import InputItem


class InputItemTiktok(InputItem):
    def __init__(self, *, resource_id, id, recognizer_data):
        super().__init__(resource_id=resource_id, recognizer_data=recognizer_data)
        self.id = id

    def download(self, filepath):
        cookie = tiktok_cookie_configured()
        api = TikTokAPI(cookie)
        api.downloadVideoById(self.id, filepath)
