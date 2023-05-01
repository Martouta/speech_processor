from .input_item import InputItem
import yt_dlp


class InputItemYoutube(InputItem):
    def __init__(self, *, resource_id, id, recognizer_data):
        super().__init__(resource_id=resource_id, recognizer_data=recognizer_data)
        self.id = id
        self.extension = 'mp4'

    def download(self, filepath):
        ydl_opts = {
            'format': 'worstvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': filepath,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={self.id}"])
