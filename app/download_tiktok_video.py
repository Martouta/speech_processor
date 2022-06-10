from TikTokApi import TikTokApi

def download_tiktok_video(reference_id, fp_tuple):
    '''
    TODO
    '''
    with TikTokApi() as api:
        video = api.video(id=reference_id)
        video_data = video.bytes()
        with open(f"{fp_tuple[0]}/{fp_tuple[1]}", 'wb') as output_file:
            output_file.write(video_data)