from TikTokAPI import TikTokAPI
from .tiktok_cookie_configured import tiktok_cookie_configured

def download_tiktok_video(reference_id, fp_tuple):
    '''
    Download video from TikTok with id in reference_id.
    Save it in the path and with the name an extension of the params in fp_tuple.
    '''
    cookie = tiktok_cookie_configured()
    api = TikTokAPI(cookie)
    api.downloadVideoById(reference_id, f"{fp_tuple[0]}/{fp_tuple[1]}")