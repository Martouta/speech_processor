from pytube import YouTube

def download_youtube_video(reference_id, fp_tuple):
    YouTube(f"youtube.com/watch?v={reference_id}") \
        .streams \
        .filter(only_audio=True, file_extension='mp4') \
        .order_by('abr') \
        .desc() \
        .first() \
        .download(output_path=fp_tuple[0], filename=fp_tuple[1])
