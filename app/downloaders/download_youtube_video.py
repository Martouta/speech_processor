from pytube import YouTube


def download_youtube_video(reference_id, dir_path, filename):
    '''
    Download video from YouTube with id in reference_id.
    Save it in the path and with the name an extension of the params in fp_tuple.
    '''
    YouTube(f"youtube.com/watch?v={reference_id}") \
        .streams \
        .filter(only_audio=True, file_extension='mp4') \
        .order_by('abr') \
        .desc() \
        .first() \
        .download(output_path=dir_path, filename=filename)
