from pytube import YouTube
from .input_item import InputItem


class InputItemYoutube(InputItem):
    def __init__(self, *, resource_id, id, recognizer_data):
        super().__init__(resource_id=resource_id, recognizer_data=recognizer_data)
        self.id = id
        self.extension = 'mp4'

    def download(self, filepath):
        YouTube(f"youtube.com/watch?v={self.id}") \
            .streams \
            .filter(only_audio=True, file_extension=self.extension) \
            .order_by('abr') \
            .desc() \
            .first() \
            .download(**InputItemYoutube.downloads_params(filepath))

    @staticmethod
    def downloads_params(filepath):
        output_path, filename = filepath.rsplit('/', 1)
        return {'output_path': output_path, 'filename': filename}
